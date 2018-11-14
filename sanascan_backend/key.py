from typing import Tuple, Iterable, List
from itertools import chain

from .word import Word

katakana_table = [
    'アイウエオヴァィゥェォ',
    'カキクケコガギグゲゴ',
    'サシスセソザジズゼゾ',
    'タチツテトッダヂヅデド',
    'ナニヌネノ',
    'ハヒフヘホバビブベボパピプペポ',
    'マミムメモ',
    'ヤユヨャュョ',
    'ラリルレロ',
    'ワヲンー'
]

NUM_TABLE = {c: idx for idx, col in enumerate(katakana_table) for c in col}


class Key():
    _tpl: Tuple[int, ...]

    @staticmethod
    def from_words(words: List[Word]) -> 'Key':
        kana_iter = chain.from_iterable([w.yomi for w in words])
        return Key(*[NUM_TABLE[i] for i in kana_iter])

    def __init__(self, *args: int) -> None:
        if not all([isinstance(i, int) for i in args]):
            raise TypeError

        self._tpl = tuple(args)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Key):
            return NotImplemented
        return self._tpl == other._tpl

    def __hash__(self) -> int:
        return hash(self._tpl)

    def __repr__(self) -> str:
        return '<Key {}>'.format(repr(self._tpl))

    def subsequence(self, start: int) -> 'Iterable[Key]':
        if start >= len(self._tpl):
            raise ValueError

        len_ = len(self._tpl)
        for i in range(start+1, len_+1):
            subtpl = self._tpl[start:i]
            yield Key(*subtpl)

    def __len__(self) -> int:
        return len(self._tpl)
