import re

import jaconv

from ....word import Word
from .... import SNKException

class SymbolError(SNKException):
    pass

class MarkError(SNKException):
    pass

class AnalyzeMorpheme:
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
        if AnalyzeMorpheme.symbol.match(self._surface):
            return True
        if self._has_yomi and AnalyzeMorpheme.symbol.match(self._yomi):
            return True
        return False

    def surface(self):
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            return self._surface
        if AnalyzeMorpheme.hira.match(self._surface):
            return self._surface
        if AnalyzeMorpheme.kata.match(self._surface):
            return self._surface

        if AnalyzeMorpheme.eng.match(self._surface):
            return Word.MARK['eng']
        if AnalyzeMorpheme.num.match(self._surface):
            return Word.MARK['num']

        return Word.MARK['unk']

    def yomi(self):
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            return self._conv_kata(self._yomi)

        surface = self.surface()
        if AnalyzeMorpheme.hira.match(surface):
            return self._conv_kata(surface)
        if AnalyzeMorpheme.kata.match(surface):
            return self._conv_kata(surface)

        if not surface in Word.MARK.values():
            raise MarkError()
        return surface

    def _conv_kata(self, str_):
        tbl = AnalyzeMorpheme.old_kana_table
        return jaconv.hira2kata(str_).translate(tbl).replace('・', '')
