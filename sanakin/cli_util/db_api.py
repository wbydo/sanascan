from contextlib import ContextDecorator
import sys
import logging

import yaml
import sqlalchemy
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy.orm.session import Session as OriginalSession
from sqlalchemy.orm import sessionmaker

from ..err import SNKException
from ..const import INSERT_DATA_NUM, MAX_QUERY_SIZE

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
        echo=False
    )

class _SNKSession(OriginalSession, ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        self.close()
        return False

    def commit_manager(self):
        return _CommitManager(self)

SNKSession = sessionmaker(class_=_SNKSession)

class _CommitManager:
    def __init__(self, snksession):
        self._s = snksession

    def __enter__(self):
        return self._s

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._s.rollback()
        else:
            self._s.commit()

        return False

def limit_select(query, class_id, *, max_req=1000):
    # 参考: https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/WindowedRangeQuery

    first_id = None
    while True:
        q = query
        if first_id is not None:
            q = query.filter(class_id > first_id)

        record = None
        for record in q.order_by(class_id).limit(max_req):
            yield record

        if record is None:
            break
        first_id = class_id.__get__(record, class_id) if record else None

def bulk_insert(iterator, klass, *, is_develop_mode=True):
    def _insert(instances):
        with SNKSession() as session:
            with session.commit_manager() as s:
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
            _insert(instances)
            instances = []
        n += 1

    if instances:
        _insert(instances)
