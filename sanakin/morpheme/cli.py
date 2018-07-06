from logging import getLogger
from itertools import zip_longest

import sqlalchemy.dialects.mysql as mysql

from .. import Morpheme
from ..mapped_classes import Sentence, Morpheme
from ..cli_util.base_function import _bulk_insert
from ..cli_util.db_api import limit_select
from ..const import MAX_SELECT_RECORD

LOGGER = getLogger(__name__)

def insert(session, mecab, *, is_develop_mode=True):
    def _iterator():
        query = session.query(Sentence)

        itr = limit_select(query, Sentence.id, max_req=MAX_SELECT_RECORD)

        for sentence in itr:
            morph_dicts = list(_morphological_analysis(mecab, sentence.text))
            length = len(morph_dicts)

            for idx, morph in enumerate(morph_dicts):
                surface = morph['surface']
                pos = morph['pos']
                yomi = morph['yomi']
                LOGGER.info(f'{sentence.sentence_id}:\t{surface}\t{yomi}\t{pos}')

                yield {
                    'nth': idx + 1,
                    'length': length,
                    'sentence_id': sentence.sentence_id,
                    'morphological_analysies_id': '{}_{:0>2}{:0>2}'.format(
                        sentence.sentence_id,
                        length,
                        idx + 1
                    ),
                    **morph
                }

    _bulk_insert(
        session,
        _iterator(),
        Morpheme,
        LOGGER,
        is_develop_mode=is_develop_mode
    )

def delete(session):
    session.query(MorphologicalAnalysis).delete()

    q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
    for t in ['morphological_analysies']:
        session.execute(q.format(t))
