from typing import NamedTuple, Iterable
from typing import Dict, List, Tuple

from enum import Enum
from enum import auto

from collections import defaultdict

from .word import Word, MARK
from .key import Key

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

num_table = {c: idx for idx, col in enumerate(katakana_table) for c in col}


class ResultOfGetByKey(NamedTuple):
    word: Word
    key: Key


class SearchFlag(Enum):
    PROCEED = auto()
    STOP = auto()


class KeyToWord():
    _datum: Dict[Key, List[Word]]
    _search_map: Dict[Key, SearchFlag]

    def __init__(self, words: List[Word]) -> None:
        self._datum = {}
        self._search_map = defaultdict(
            lambda: SearchFlag.STOP)

        for word in words:
            key = Key(*yomi2tuple(word.yomi))

            self._add_data(key, word)

    def _add_data(self, key: Key, word: Word) -> None:
        if not (key in self._datum.keys()):
            self._datum[key] = []
        self._datum[key].append(word)

        for subkey in key.subsequence(0):
            self._search_map[subkey] = SearchFlag.PROCEED

    def get_by_key(self, key: Key, start: int) -> Iterable[ResultOfGetByKey]:
        if not isinstance(key, Key):
            raise TypeError

        for subkey in key.subsequence(start):
            if self._search_map[subkey] == SearchFlag.STOP:
                break
            if subkey in self._datum.keys():
                for word in self._datum[subkey]:
                    yield ResultOfGetByKey(word=word, key=subkey)


def yomi2tuple(yomi: str) -> Tuple[int, ...]:
    if yomi in MARK.values():
        raise ValueError()
    return tuple([num_table[i] for i in yomi])
