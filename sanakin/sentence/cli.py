from logging import getLogger
import sys

import sqlalchemy.dialects.mysql as mysql

from ..mapped_classes import SentenceDelimiter, CorpusData, Sentence
from ..cli_util.base_function import _bulk_insert

LOGGER = getLogger(__name__)

def insert(
    session,
    sentence_delimiter_id,
    *,
    is_develop_mode=True
):

    def _iterator():
        delimiter = session.query(SentenceDelimiter).filter(
            SentenceDelimiter.sentence_delimiter_id == sentence_delimiter_id
        ).one()

        q = session.query(CorpusData)

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

    insert_stmt = mysql.insert(Sentence)
    insert_stmt = insert_stmt.on_duplicate_key_update(
        corpus_data_id=insert_stmt.inserted.corpus_data_id,
        sentence_delimiter_id=insert_stmt.inserted.sentence_delimiter_id,
        text=insert_stmt.inserted.text,
        nth=insert_stmt.inserted.nth,
        length=insert_stmt.inserted.length
    )

    _bulk_insert(
        session,
        _iterator(),
        Sentence,
        LOGGER,
        is_develop_mode=is_develop_mode
    )
