from logging import getLogger

LOGGER = getLogger(__name__)

import re
import jaconv
from hashlib import sha1
from pathlib import Path

from ..word import Word
from ..srilm import srilm
from ..next_id import NextIdSearchable

class BaseLangModel(NextIdSearchable):
    @classmethod
    def create(klass, sentences, mecab, lang_model_file_dir):
        wakati =  '\n'.join(
            klass._process_multi_sentences(sentences, mecab)
        )

        arpa_string =  srilm(wakati, 3)
        checksum = sha1(arpa_string).digest()
        lang_model_id = klass.next_id('lang_model_id', 'LM', 4)

        path = Path(lang_model_file_dir) / (lang_model_id + '.txt')

        with path.open('w') as f:
            f.write(arpa_string.decode('utf-8'))

        return klass(lang_model_id=lang_model_id, checksum=checksum)

    @classmethod
    def _process_multi_sentences(klass, multi_sentence, mecab):
        for sentence in multi_sentence:

            # iterのまま返す必要が出てくるかもしれないのでこう書いておく
            iter_ = klass._process_single_sentence(sentence, mecab)
            yield ' '.join(iter_)

    @classmethod
    def _process_single_sentence(klass, single_sentence, mecab):
        normalized = jaconv.normalize(single_sentence)
        for mec_node in mecab.parse(normalized, as_nodes=True):
            if mec_node.is_eos():
                break

            res = _AnalyzeMorp(mec_node)
            if res.is_symbol():
                continue

            # Word型で返す必要が出てくるかもしれないのでこう書いておく
            w = Word(surface=res.surface(), yomi=res.yomi())
            yield str(w)


class SymbolError(Exception):
    pass

class MarkError(Exception):
    pass

class _AnalyzeMorp:
    symbol = re.compile(r'^(?:\W|_|・)+$')

    hira = re.compile(r'^[ぁ-ゔ]+$')
    kata = re.compile(r'^(?:[ァ-ヶヰヱヵヮ]|ー|・)+$')

    eng = re.compile(r'^[a-zA-Zａ-ｚＡ-Ｚ]+$')
    num = re.compile(r'^[0-9０-９]+$')

    old_kana_table = str.maketrans('ヰヱヵヶヮ', 'イエカケワ')

    def __init__(self, mecab_node):
        self.features = mecab_node.feature.split(',')
        self.hinshi = self.features[0]

        self._surface = mecab_node.surface
        self._has_yomi = True if len(self.features) >=8 else False

        if self._has_yomi:
            self._yomi = self.features[7]

    def is_symbol(self):
        if self.hinshi == '記号':
            return True
        if _AnalyzeMorp.symbol.match(self._surface):
            return True
        if self._has_yomi and _AnalyzeMorp.symbol.match(self._yomi):
            return True
        return False

    def surface(self):
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            return self._surface
        if _AnalyzeMorp.hira.match(self._surface):
            return self._surface
        if _AnalyzeMorp.kata.match(self._surface):
            return self._surface

        if _AnalyzeMorp.eng.match(self._surface):
            return Word.MARK['eng']
        if _AnalyzeMorp.num.match(self._surface):
            return Word.MARK['num']

        return Word.MARK['unk']

    def yomi(self):
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            return self._conv_kata(self._yomi)

        surface = self.surface()
        if _AnalyzeMorp.hira.match(surface):
            return self._conv_kata(surface)
        if _AnalyzeMorp.kata.match(surface):
            return self._conv_kata(surface)

        if not surface in Word.MARK.values():
            raise MarkError()
        return surface

    def _conv_kata(self, str_):
        tbl = _AnalyzeMorp.old_kana_table
        return jaconv.hira2kata(str_).translate(tbl).replace('・', '')
