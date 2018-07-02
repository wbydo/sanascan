from logging import getLogger
from itertools import zip_longest

import sqlalchemy.dialects.mysql as mysql

from ..mapped_classes import Sentence, MorphologicalAnalysis
from ..cli_util.base_function import _bulk_insert
from ..cli_util.db_api import limit_select

LOGGER = getLogger(__name__)

def insert(session, mecab, *, is_develop_mode=True):
    def _iterator():
        query = session.query(Sentence)

        itr = limit_select(query, Sentence.id, max_req=5)

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
        MorphologicalAnalysis,
        LOGGER,
        is_develop_mode=is_develop_mode
    )

def delete(session):
    query = session.query(MorphologicalAnalysis).delete()

def _morphological_analysis(mecab, text):
    for mnode in mecab.parse(text, as_nodes=True):
        if mnode.is_eos():
            break

        keys = ['pos', 'pos1', 'pos2', 'pos3', 'ctype', 'cform', 'base', 'yomi', 'pron']
        features = [f if not f == '*' else None for f in mnode.feature.split(',')]
        yield {
            'surface': mnode.surface,
            **dict(zip_longest(keys, features))
        }
