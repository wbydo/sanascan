from logging import getLogger
import sys

import sqlalchemy.dialects.mysql as mysql

from .. import SentenceDelimiter, CorpusData, Sentence

LOGGER = getLogger(__name__)

def insert(
    session,
    engine,
    sentence_delimiter_id,
    is_develop_mode):

    def _iterate():
        delimiter = session.query(SentenceDelimiter).filter(
            SentenceDelimiter.sentence_delimiter_id == sentence_delimiter_id
        ).one()

        q = session.query(CorpusData)

        i = 0
        for data in q:
            for sentence in delimiter.split(data.text):
                result = {
                    'corpus_data_id': data.corpus_data_id,
                    'sentence_id': '{}_{}_{:0>2}{:0>2}'.format(
                        data.corpus_data_id,
                        delimiter.sentence_delimiter_id,
                        sentence['length'],
                        sentence['nth']
                    ),
                    **sentence
                }
                LOGGER.info('{}:\t{}'.format(
                    result['sentence_id'],
                    result['text']
                ))
                yield result
                i += 1
                if is_develop_mode and i >= 100:
                    raise StopIteration()

    def _insert(sentence_dict):
        insert_stmt = mysql.insert(Sentence)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            corpus_data_id=insert_stmt.inserted.corpus_data_id,
            sentence_delimiter_id=insert_stmt.inserted.sentence_delimiter_id,
            text=insert_stmt.inserted.text,
            nth=insert_stmt.inserted.nth,
            length=insert_stmt.inserted.length
        )
        with engine.begin() as conn:
            conn.execute(on_duplicate_key_stmt, sentence_dict)

    sentences = []
    max_size = 500_000_000
    for s in _iterate():
        if sys.getsizeof(sentences) < max_size:
            sentences.append(s)
        else:
            LOGGER.info(f'INSERT: {len(sentences)}件挿入!!!')
            _insert(sentences)
            sentences = []
    if sentences:
        LOGGER.info(f'INSERT: {len(sentences)}件挿入!!!')
        _insert(sentences)
    session.commit()
