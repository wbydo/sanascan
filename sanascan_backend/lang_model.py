import re
from typing import NamedTuple, Dict, List, Set
from typing import Pattern, ClassVar, KeysView
from enum import Enum
from enum import auto
from itertools import chain

from .word import Word


class ArpaArea(Enum):
        DATA = auto()
        NGRAM = auto()


class NgramError(Exception):
    pass


class ParseError(Exception):
    pass


class LangModel:
    class Data(NamedTuple):
        prob: float
        backoff: float

    remove_head: ClassVar[Pattern] = re.compile(r'^(?:.*?) (?P<target>.*)$')
    remove_tail: ClassVar[Pattern] = re.compile(r'^(?P<target>.*) (?:.*?)$')

    _dic: Dict[str, Data]
    _keys: KeysView[str]

    def __init__(self, arpa_text: str) -> None:
        self._dic = self._process_arpa_file(arpa_text)
        self._keys = self._dic.keys()

    def _process_arpa_file(self, arpa_text: str) -> Dict[str, Data]:
        title = re.compile(r'^\\(\d)-grams:$')
        area = ArpaArea.DATA

        result = {}
        for unstriped_line in arpa_text.split('\n'):
            line = unstriped_line.strip()
            m = title.match(line)
            if m:
                    area = ArpaArea.NGRAM
                    ngram = int(m.group(1))
                    continue

            if area == ArpaArea.DATA or line == '' or line == '\\end\\':
                    continue

            data_line = line.split('\t')
            prob = float(data_line[0])
            word = data_line[1]
            backoff = float(data_line[2]) if len(data_line) == 3 else 0
            result[word] = LangModel.Data(prob=prob, backoff=backoff)
        self._order = ngram
        return result

    def score(self, words: List[Word]) -> float:
        len_ = len(words)
        if len_ > self._order:
            raise NgramError(Word.to_str(words))

        if len_ == 1 and (not str(words[0]) in self._keys):
            raise NgramError(str(words[0]) + 'は使用言語モデルの語彙にない')

        if Word.to_str(words) in self._keys:
            return self._dic[Word.to_str(words)].prob
        else:
            context = Word.to_str(words[:-1])
            p = self.score(words[1:])

            if context in self._keys:
                backoff = self._dic[context].backoff
                return backoff + p
            else:
                return p

    def get_vocab(self) -> Set[Word]:
        return set(chain.from_iterable(
            [Word.from_str_of_multiword(k) for k in self._dic.keys()]
        ))
