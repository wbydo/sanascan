from itertools import zip_longest
from logging import getLogger

LOGGER = getLogger(__name__)

class BaseMopheme:
    @classmethod
    def create(klass, sentence, mecab):
        morph_dicts = list(klass._morphological_analysis(mecab, sentence.text))
        length = len(morph_dicts)

        for idx, morph in enumerate(morph_dicts):
            # LOGGERのためだけの処理
            surface = morph['surface']
            pos = morph['pos']
            yomi = morph['yomi']
            LOGGER.info(f'{sentence.sentence_id}:\t{surface}\t{yomi}\t{pos}')

            yield klass(**{
                'nth': idx + 1,
                'length': length,
                'sentence_id': sentence.sentence_id,
                'morpheme_id': '{}_{:0>2}{:0>2}'.format(
                    sentence.sentence_id,
                    length,
                    idx + 1,
                ),
                **morph,
            })

    @classmethod
    def _morphological_analysis(klass, mecab, text):
        for mnode in mecab.parse(text, as_nodes=True):
            if mnode.is_eos():
                break

            keys = ['pos', 'pos1', 'pos2', 'pos3', 'ctype', 'cform', 'base', 'yomi', 'pron']
            features = [f if not f == '*' else None for f in mnode.feature.split(',')]
            yield {
                'surface': mnode.surface,
                **dict(zip_longest(keys, features))
            }
