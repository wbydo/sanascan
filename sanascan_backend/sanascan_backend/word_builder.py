from typing import Dict, List, ClassVar, Pattern, Optional, cast, Iterable

import re

import jaconv
from natto import MeCab, MeCabNode

from .word import Word, TagWord


class SymbolError(Exception):
    pass


class MarkError(Exception):
    pass


class WordBuilder:
    symbol: ClassVar[Pattern] = re.compile(r'^(?:\W|_|・|◇)+$')

    hira: ClassVar[Pattern] = re.compile(r'^[ぁ-ゔ]+$')
    kata: ClassVar[Pattern] = re.compile(r'^(?:[ァ-ヶヰヱヵヮ]|ー|・)+$')

    eng: ClassVar[Pattern] = re.compile(r'^[a-zA-Zａ-ｚＡ-Ｚ]+$')
    num: ClassVar[Pattern] = re.compile(r'^[0-9０-９]+$')

    old_kana_table: ClassVar[Dict[int, Optional[int]]]\
        = str.maketrans('ヰヱヵヶヮ', 'イエカケワ')

    _hinshi: str
    _surface: str
    _has_yomi: bool
    _yomi: Optional[str]

    def __init__(self) -> None:
        raise NotImplementedError()

    def is_symbol(self) -> bool:
        if self._hinshi == '記号':
            return True
        if WordBuilder.symbol.match(self._surface):
            return True
        if self._has_yomi and WordBuilder.symbol.match(self._yomi):
            return True
        return False

    def to_word(self) -> Optional[Word]:
        if self.is_symbol():
            return None

        surface = self._formal_surface()

        if TagWord.is_include(self._formal_surface()):
            return TagWord(surface)
        else:
            yomi = self._formal_yomi()
            return Word(surface=surface, yomi=yomi)

    def _formal_surface(self) -> str:
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            return self._surface
        if WordBuilder.hira.match(self._surface):
            return self._surface
        if WordBuilder.kata.match(self._surface):
            return self._surface

        if WordBuilder.eng.match(self._surface):
            return TagWord('<eng>').surface
        if WordBuilder.num.match(self._surface):
            return TagWord('<num>').surface

        return TagWord('<unk>').surface

    def _formal_yomi(self) -> str:
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            assert self._yomi is not None
            return self._conv_kata(self._yomi)

        surface = self._formal_surface()
        if WordBuilder.hira.match(surface):
            return self._conv_kata(surface)
        if WordBuilder.kata.match(surface):
            return self._conv_kata(surface)

        # if not (surface in MARK.values()):
        if not TagWord.is_include(surface):
            raise MarkError()
        return surface

    def _conv_kata(self, str_: str) -> str:
        tbl = WordBuilder.old_kana_table
        katakana = cast(str, jaconv.hira2kata(str_))
        return katakana.translate(tbl).replace('・', '')


class BuilderFromMeCab(WordBuilder):
    def __init__(self, mecab_node: MeCabNode) -> None:
        features: List[str] = mecab_node.feature.split(',')
        self._hinshi = features[0]

        self._surface = mecab_node.surface
        self._has_yomi = True if len(features) >= 8 else False

        if self._has_yomi:
            self._yomi = features[7]

    @classmethod
    def from_plaintext(
            klass,
            text: str,
            mecab: MeCab,
            ) -> 'Iterable[Word]':

        normalized = jaconv.normalize(text)
        for mec_node in mecab.parse(normalized, as_nodes=True):
            if mec_node.is_eos():
                break

            w = klass(mec_node).to_word()
            if w is None:
                continue

            yield w
