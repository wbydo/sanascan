from logging import getLogger
from itertools import zip_longest

import sqlalchemy.dialects.mysql as mysql

from ..mapped_classes import Sentence, MorphologicalAnalysis
from ..cli_util.base_function import _bulk_insert

LOGGER = getLogger(__name__)

def insert(session, mecab, is_develop_mode):
    def _iterator():
        query = session.query(Sentence)

        for sentence in query:
            morph_dicts = list(_morphological_analysis(mecab, sentence.text))
            length = len(morph_dicts)

            for idx, morph in enumerate(morph_dicts):
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
