import sys

from sqlalchemy.exc import IntegrityError
import sqlalchemy.dialects.mysql as mysql

from ..const import INSERT_DATA_NUM, MAX_QUERY_SIZE
from ..err import SNKException

def _simple_insert(klass, logger, *column_names):
    def _insert(session, *attr):
        d = dict(zip(column_names, attr))

        m = klass(**d)

        try:
            session.add(m)
            session.commit()
        except IntegrityError as e:
            err_code, _ = e.orig.args
            if err_code == 1062:
                logger.info('格納済み')
                session.rollback()
            else:
                raise e

    return _insert

def _simple_delete(klass, *column_names):
    def _delete(session, *attr):
        d = dict(zip(column_names, attr))

        m = session.query(klass).filter_by(**d)
        m.delete()

    return _delete

def _bulk_insert(
    session,
    iterator,
    klass,
    logger,
    is_develop_mode=True,
    ignore_columns=None,
):

    ic = ignore_columns if ignore_columns else []
    columns = klass.__table__.columns.keys()
    no_column = set(ic) - set(columns)
    if no_column:
        raise SNKException(','.join(no_column) + f'は{klass}のカラムにない')

    ic.append('id')
    for c in ic:
        columns.remove(c)

    insert_stmt = mysql.insert(klass)
    insert_stmt = insert_stmt.on_duplicate_key_update(
        **dict([(c, insert_stmt.inserted[c]) for c in columns])
    )

    def _insert(instances):
        session.execute(insert_stmt, instances)
        logger.info(f'INSERT: {len(instances)}件挿入!!!')

    instances = []

    n = 0
    for i in iterator:
        if is_develop_mode and n >= INSERT_DATA_NUM:
            break

        if sys.getsizeof(instances) < MAX_QUERY_SIZE:
            instances.append(i)
        else:
            _insert(instances)
            instances = []
        n += 1

    if instances:
        _insert(instances)
