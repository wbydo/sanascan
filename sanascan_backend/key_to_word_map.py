from typing import NamedTuple, Iterable
from typing import Dict, List

from enum import Enum
from enum import auto

from collections import defaultdict

from .word import Word
from .key import Key


class ResultOfGetByKey(NamedTuple):

    word: Word
    key: Key


class SearchFlag(Enum):
    PROCEED = auto()
    STOP = auto()


class KeyToWordMap():
    _datum: Dict[Key, List[Word]]
    _search_map: Dict[Key, SearchFlag]

    def __init__(self, words: List[Word]) -> None:
        self._datum = {}
        self._search_map = defaultdict(
            lambda: SearchFlag.STOP)

        for word in words:
            key = Key.from_words([word])

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
