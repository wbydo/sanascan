from typing import Tuple, Iterable, Union, Iterator, NewType, Dict
from typing import Optional, Generic, TypeVar, Type, ClassVar

from .word import TagWord, Sentence
from .yomi_property import YomiProperty, ColNum, Position

katakana_table = [
    'アイウエオヴァィゥェォ',
    'カキクケコガギグゲゴ',
    'サシスセソザジズゼゾ',
    'タチツテトダヂヅデド',
    'ナニヌネノ',
    'ハヒフヘホバビブベボパピプペポ',
    'マミムメモ',
    'ヤユヨ',
    'ラリルレロ',
    'ワヲン',
    'ャュョッー'
]

Yomi = NewType('Yomi', str)

T = TypeVar('T', ColNum, Position)


class Key(Generic[T]):
    _tpl: Tuple[Union[TagWord, T], ...]

    _trans: ClassVar[Dict[int, Optional[int]]] = {}
    _trans.update(str.maketrans('ヴァィゥェォ', 'ウアイウエオ'))
    _trans.update(str.maketrans('ガギグゲゴ', 'カキクケコ'))
    _trans.update(str.maketrans('ザジズゼゾ', 'サシスセソ'))
    _trans.update(str.maketrans('ダヂヅデド', 'タチツテト'))
    _trans.update(str.maketrans('バビブベボパピプペポ', 'ハヒフヘホハヒフヘホ'))

    _TABLE: ClassVar[Dict[Yomi, YomiProperty]] = {}
    for idx, col in enumerate(katakana_table):
        for c in col:
            pos = c.translate(_trans)
            _TABLE[Yomi(c)] = YomiProperty(
                col=idx,
                pos=pos
            )

    @classmethod
    def from_sentence(
            klass,
            sentence: Sentence,
            type_: Type[T]
            ) -> 'Key':

        return klass(klass._process_words(sentence, type_))

    @classmethod
    def _process_words(
            klass,
            sentence: Sentence,
            type_: Type[T],
            ) -> Iterable[Union[TagWord, T]]:

        for w in sentence.words:
            if isinstance(w, TagWord):
                yield w
            else:
                for c in w.yomi:
                    y = Yomi(c)
                    yield type_.create(klass._TABLE[y])

    @classmethod
    def from_int(klass, arg: Iterable[Union[TagWord, int]]) -> 'Key[ColNum]':
        return Key[ColNum](
            i if isinstance(i, TagWord) else ColNum(i) for i in arg
        )

    @classmethod
    def from_str(klass, arg: Iterable[Union[TagWord, str]]) -> 'Key[Position]':
        return Key[Position](
            i if isinstance(i, TagWord) else Position(i) for i in arg
        )

    def __init__(self, arg: Iterable[Union[TagWord, T]]) -> None:
        self._tpl = tuple(arg)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Key):
            return NotImplemented
        return self._tpl == other._tpl

    def __hash__(self) -> int:
        return hash(self._tpl)

    def __repr__(self) -> str:
        return '<Key {}>'.format(repr(self._tpl))

    def __str__(self) -> str:
        if not len(self) == 1:
            raise TypeError('lenが1のときしかstrできない')
        return str(self._tpl[0])

    def __iter__(self) -> 'Iterator[Key]':
        for i in self._tpl:
            yield Key([i])

    def __add__(self, other: 'Key') -> 'Key':
        return Key(self._tpl + other._tpl)

    def subsequence_with_end(self, end: int) -> 'Iterable[Key]':
        len_ = len(self._tpl)
        if end > len_ - 1 or end < 0:
            raise ValueError()

        for i in reversed(range(end+1)):
            subtpl = self._tpl[i:end+1]
            yield Key(subtpl)

    def all_of_subsequence(self) -> 'Iterable[Key]':
        return self.subsequence_with_end(len(self)-1)

    def __len__(self) -> int:
        return len(self._tpl)
