from typing import Tuple, Iterable, List, Union

from .word import Word, TagWord

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
    _tpl: Tuple[Union[TagWord, int], ...]

    @classmethod
    def from_words(klass, words: List[Word]) -> 'Key':
        return Key(klass._process_words(words))

    @staticmethod
    def _process_words(words: List[Word]) -> Iterable[Union[TagWord, int]]:
        for w in words:
            if isinstance(w, TagWord):
                yield w
            else:
                for c in w.yomi:
                    yield NUM_TABLE[c]

    def __init__(self, args: Iterable[Union[TagWord, int]]) -> None:

        self._tpl = tuple(args)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Key):
            return NotImplemented
        return self._tpl == other._tpl

    def __hash__(self) -> int:
        return hash(self._tpl)

    def __repr__(self) -> str:
        return '<Key {}>'.format(repr(self._tpl))

    def subsequence_with_end(self, end: int) -> 'Iterable[Key]':
        len_ = len(self._tpl)
        if end > len_ - 1 or end < 0:
            raise ValueError()

        for i in range(end+1):
            subtpl = self._tpl[i:end+1]
            yield Key(subtpl)

    def all_of_subsequence(self) -> 'Iterable[Key]':
        return self.subsequence_with_end(len(self)-1)

    def __len__(self) -> int:
        return len(self._tpl)
