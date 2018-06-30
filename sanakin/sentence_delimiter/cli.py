from logging import getLogger

from sqlalchemy.exc import IntegrityError

from .. import SentenceDelimiter

LOGGER = getLogger(__name__)

def insert(session, regex, sentence_delimiter_id):
    d = SentenceDelimiter(
        regex=regex,
        sentence_delimiter_id=sentence_delimiter_id,)

    try:
        session.add(d)
        session.commit()
    except IntegrityError as e:
        err_code, _ = e.orig.args
        if err_code == 1062:
            LOGGER.info('格納済み')
            session.rollback()
        else:
            raise e

def delete(session, sentence_delimiter_id):
    d = session.query(SentenceDelimiter).filter(
        SentenceDelimiter.sentence_delimiter_id == sentence_delimiter_id
    )

    d.delete()
    session.commit()
