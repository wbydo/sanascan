from typing import NamedTuple, Iterable
from typing import Dict, List, Set

from enum import Enum
from enum import auto

from collections import defaultdict

from .word import Word, Sentence
from .key import Key
from .yomi_property import ColNum, Position


class ResultOfGetByKey(NamedTuple):
    word: Word
    key: Key


class SearchFlag(Enum):
    PROCEED = auto()
    STOP = auto()


class Vocabulary():
    _datum: Dict[Key, List[Word]]
    _search_map: Dict[Key, SearchFlag]

    def __init__(self, words: Set[Word]) -> None:
        self._datum = {}
        self._search_map = defaultdict(
            lambda: SearchFlag.STOP)

        for word in words:
            for t in [ColNum, Position]:
                s = Sentence.from_iter([word])
                key = Key.from_sentence(s, t)
                self._add_data(key, word)

    def _add_data(self, key: Key, word: Word) -> None:
        if not (key in self._datum.keys()):
            self._datum[key] = []
        self._datum[key].append(word)

        for subkey in key.all_of_subsequence():
            self._search_map[subkey] = SearchFlag.PROCEED

    def get_by_key(self, key: Key) -> Iterable[ResultOfGetByKey]:
        if not isinstance(key, Key):
            raise TypeError

        for subkey in key.all_of_subsequence():
            if self._search_map[subkey] == SearchFlag.STOP:
                break
            if subkey in self._datum.keys():
                for word in self._datum[subkey]:
                    yield ResultOfGetByKey(word=word, key=subkey)
