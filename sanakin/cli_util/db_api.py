import sys
import logging

import yaml
import sqlalchemy
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy.exc import IntegrityError

from ..err import SNKException
from ..const import INSERT_DATA_NUM, MAX_QUERY_SIZE
from ..const import MAX_SELECT_RECORD
from ..snksession import SNKSession

LOGGER = logging.getLogger(__name__)

def create_engine(file_path, environment):
    with open(file_path) as f:
        config = yaml.load(f)

    if not environment in config.keys():
        raise SNKException(f'環境名{environment}が見つからない')

    db = 'mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8'.format(
        **config[environment]
    )

    return sqlalchemy.create_engine(
        db,
        encoding='utf-8',
        echo=False,
        pool_size=20,
        max_overflow=10
    )

def limit_select(query, class_id):
    # 参考: https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/WindowedRangeQuery

    first_id = None
    while True:
        with SNKSession() as session:
            q = query.with_session(session)

        if first_id is not None:
            q = query.filter(class_id > first_id)

        record = None
        for record in q.order_by(class_id).limit(MAX_SELECT_RECORD):
            yield record

        if record is None:
            break
        first_id = class_id.__get__(record, class_id) if record else None

def simple_insert(instance):
    i = instance

    with SNKSession() as session:
        try:
            session.add(i)
            session.commit()
        except IntegrityError as e:
            err_code, _ = e.orig.args
            if err_code == 1062:
                LOGGER.info('格納済み')
                session.rollback()
            else:
                raise e

def bulk_insert(iterator, klass, *, is_develop_mode=True):
    def _insert(insert_stmt, instances):
        with SNKSession() as session:
            with session.commit_manager() as s:
                LOGGER.debug(s.bind.pool.status())
                s.execute(insert_stmt, instances)
                LOGGER.info(f'INSERT: [{klass.__name__}]{len(instances)}件挿入!!!')

    insert_stmt = mysql.insert(klass)
    insert_stmt = insert_stmt.on_duplicate_key_update(
        id=insert_stmt.inserted.id
    )

    instances = []

    n = 0
    for i in iterator:
        if is_develop_mode and n >= INSERT_DATA_NUM:
            break

        if sys.getsizeof(instances) < MAX_QUERY_SIZE:
            instances.append(i.__dict__)
        else:
            LOGGER.debug('log-1')
            _insert(insert_stmt, instances)
            instances = []
        n += 1

    if instances:
        LOGGER.debug('log-2:')
        _insert(insert_stmt, instances)
