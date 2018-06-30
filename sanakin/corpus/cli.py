from logging import getLogger

from sqlalchemy.exc import IntegrityError

from .. import Corpus

LOGGER = getLogger(__name__)

def insert(session, cname, corpus_id):
    c = Corpus(
        name=cname,
        corpus_id=corpus_id,)

    try:
        session.add(c)
        session.commit()
    except IntegrityError as e:
        err_code, _ = e.orig.args
        if err_code == 1062:
            LOGGER.info('格納済み')
            session.rollback()
        else:
            raise e
