import re
from typing import Dict, List, ClassVar, Pattern, Optional, Tuple
from typing import Iterable, cast

from natto import MeCab, MeCabNode
import jaconv

DELIMITER: str = '/'
# MARK: Dict[str, str] = {
#     'unk': '<unk>',
#     'eng': '<eng>',
#     'num': '<num>',
#     '<s>': '<s>',  # 要検討
# }


class SymbolError(Exception):
    pass


class MarkError(Exception):
    pass


class Word:
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

            if TagWord.is_include(res.surface()):
                yield TagWord(res.surface())
            else:
                yield Word(surface=res.surface(), yomi=res.yomi())

    @staticmethod
    def from_str_of_singleword(arg: str) -> 'Word':
        if TagWord.is_include(arg):
            return TagWord(arg)

        list_ = arg.split(DELIMITER)
        if len(list_) >= 3:
            raise ValueError

        return Word(surface=list_[0], yomi=list_[1])

    @staticmethod
    def to_str(words: 'List[Word]') -> str:
        return ' '.join([str(w) for w in words])

    def __init__(self, surface: str, yomi: str) -> None:
        self.surface = surface
        self.yomi = yomi

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return NotImplemented

        klass = self.__class__
        if not isinstance(other, klass):
            return False
        return self.__tuple__() == other.__tuple__()

    def __hash__(self) -> int:
        return hash(self.__tuple__())

    def __tuple__(self) -> Tuple[str, str]:
        return (self.surface, self.yomi)

    def __str__(self) -> str:
        return f'{self.surface}{DELIMITER}{self.yomi}'

    def __repr__(self) -> str:
        return f'Word(\'{self.surface}\',\'{self.yomi}\')'


class TagWord(Word):
    _tags: ClassVar[List[str]] = ['<unk>', '<eng>', '<num>', '<s>', '</s>']

    @classmethod
    def is_include(klass, arg: str) -> bool:
        return arg in klass._tags

    def __init__(self, arg: str) -> None:
        if arg not in self._tags:
            raise ValueError(arg)
        super(self.__class__, self).__init__(surface=arg, yomi=arg)


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
            return TagWord('<eng>').surface
        if AnalyzeMorp.num.match(self._surface):
            return TagWord('<num>').surface

        return TagWord('<unk>').surface

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

        # if not (surface in MARK.values()):
        if not TagWord.is_include(surface):
            raise MarkError()
        return surface

    def _conv_kata(self, str_: str) -> str:
        tbl = AnalyzeMorp.old_kana_table
        katakana = cast(str, jaconv.hira2kata(str_))
        return katakana.translate(tbl).replace('・', '')
