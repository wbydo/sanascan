import re

import jaconv
from natto import MeCab

from ....word import Word
from .analize_morpheme import AnalyzeMorpheme

STOP_SYMBOL = re.compile(r'[。．\.！!？\?\n]+')

def split(multi_sentence):
    normalized = jaconv.normalize(multi_sentence)
    for sentence in re.split(STOP_SYMBOL, normalized):
        striped = sentence.strip()
        if striped:
            word_iter = _process_sentence(striped)
            yield ' '.join(map(str, word_iter))

def _process_sentence(sentence):
    mecab = MeCab()
    for mec_node in mecab.parse(sentence, as_nodes=True):
        if mec_node.is_eos():
            break

        res = AnalyzeMorpheme(mec_node)
        if res.is_symbol():
            continue
        yield Word(surface=res.surface(), yomi=res.yomi())
