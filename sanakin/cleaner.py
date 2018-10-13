from enum import Enum
import re

import jaconv

from .word import Word

class Cleaner:
    stop_symbol = re.compile(r'(?P<period>(?:。|．|\.|！|!|？|\?)+)')

    def clean(self, sentences, mecab):
        for sentence in sentences:
            normalized = jaconv.normalize(sentence)
            yield self._process_sentence(sentence, mecab)

    def _process_sentence(self, sentence, mecab):
        for mec_node in mecab.parse(sentence, as_nodes=True):
            if mec_node.is_eos():
                break

            res = _AnalyzeMorp(mec_node)
            if res.is_symbol():
                continue
            yield Word(surface=res.surface(), yomi=res.yomi())

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
