import sys

from sqlalchemy.exc import IntegrityError

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
