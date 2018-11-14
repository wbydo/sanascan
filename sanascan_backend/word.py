import re
from typing import NamedTuple, Dict, List, ClassVar, Pattern, Optional
from typing import Iterable, cast

from natto import MeCab, MeCabNode
import jaconv

DELIMITER: str = '/'
MARK: Dict[str, str] = {
    'unk': '<unk>',
    'eng': '<eng>',
    'num': '<num>',
    '<s>': '<s>',  # 要検討
}


class SymbolError(Exception):
    pass


class MarkError(Exception):
    pass


class Word(NamedTuple):
    surface: str
    yomi: str

    @staticmethod
    def from_wakachigaki(wakachigaki: str) -> 'List[Word]':
        return [Word.from_str_of_singleword(w) for w in wakachigaki.split(' ')]

    @classmethod
    def from_sentence(klass, sentence: str, mecab: MeCab) -> 'Iterable[Word]':
        normalized = jaconv.normalize(sentence)
        for mec_node in mecab.parse(normalized, as_nodes=True):
            if mec_node.is_eos():
                break

            res = AnalyzeMorp(mec_node)
            if res.is_symbol():
                continue

            yield Word(surface=res.surface(), yomi=res.yomi())

    @staticmethod
    def from_str_of_singleword(arg: str) -> 'Word':
        if arg in MARK.values():
            return Word(surface=arg, yomi=arg)

        list_ = arg.split(DELIMITER)
        if len(list_) >= 3:
            raise ValueError

        return Word(surface=list_[0], yomi=list_[1])

    @staticmethod
    def to_str(words: 'List[Word]') -> str:
        return ' '.join([str(w) for w in words])

    def __str__(self) -> str:
        if self.surface in MARK.values():
            return self.surface
        return f'{self.surface}{DELIMITER}{self.yomi}'

    def __repr__(self) -> str:
        return f'Word(\'{self.surface}\',\'{self.yomi}\')'


class AnalyzeMorp:
    symbol: ClassVar[Pattern] = re.compile(r'^(?:\W|_|・)+$')

    hira: ClassVar[Pattern] = re.compile(r'^[ぁ-ゔ]+$')
    kata: ClassVar[Pattern] = re.compile(r'^(?:[ァ-ヶヰヱヵヮ]|ー|・)+$')

    eng: ClassVar[Pattern] = re.compile(r'^[a-zA-Zａ-ｚＡ-Ｚ]+$')
    num: ClassVar[Pattern] = re.compile(r'^[0-9０-９]+$')

    old_kana_table: ClassVar[Dict[int, Optional[int]]]\
        = str.maketrans('ヰヱヵヶヮ', 'イエカケワ')

    features: List[str]
    hinshi: str
    _surface: str
    _has_yomi: bool
    _yomi: Optional[str]

    def __init__(self, mecab_node: MeCabNode) -> None:
        self.features = mecab_node.feature.split(',')
        self.hinshi = self.features[0]

        self._surface = mecab_node.surface
        self._has_yomi = True if len(self.features) >= 8 else False

        if self._has_yomi:
            self._yomi = self.features[7]

    def is_symbol(self) -> bool:
        if self.hinshi == '記号':
            return True
        if AnalyzeMorp.symbol.match(self._surface):
            return True
        if self._has_yomi and AnalyzeMorp.symbol.match(self._yomi):
            return True
        return False

    def surface(self) -> str:
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            return self._surface
        if AnalyzeMorp.hira.match(self._surface):
            return self._surface
        if AnalyzeMorp.kata.match(self._surface):
            return self._surface

        if AnalyzeMorp.eng.match(self._surface):
            return MARK['eng']
        if AnalyzeMorp.num.match(self._surface):
            return MARK['num']

        return MARK['unk']

    def yomi(self) -> str:
        if self.is_symbol():
            raise SymbolError()

        if self._has_yomi:
            if self._yomi is None:
                raise Exception(
                    '''
                    self._has_yomi == True のとき
                    self._yomi != Noneなので
                    このエラーが起こることはあり得ない。はず。
                    '''
                )

            return self._conv_kata(self._yomi)

        surface = self.surface()
        if AnalyzeMorp.hira.match(surface):
            return self._conv_kata(surface)
        if AnalyzeMorp.kata.match(surface):
            return self._conv_kata(surface)

        if not (surface in MARK.values()):
            raise MarkError()
        return surface

    def _conv_kata(self, str_: str) -> str:
        tbl = AnalyzeMorp.old_kana_table
        return cast(str, jaconv.hira2kata(str_)).translate(tbl).replace('・', '')
