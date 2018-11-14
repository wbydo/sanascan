import re
from typing import NamedTuple, Dict, Set, Tuple, Iterable
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

    _dic: Dict[Tuple[Word, ...], Data]

    def __init__(self, arpa_text: str) -> None:
        self._dic = self._process_arpa_file(arpa_text)

    def _process_arpa_file(
            self,
            arpa_text: str
            ) -> Dict[Tuple[Word, ...], Data]:

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
            word = tuple(Word.from_wakachigaki(data_line[1]))
            backoff = float(data_line[2]) if len(data_line) == 3 else 0
            result[word] = LangModel.Data(prob=prob, backoff=backoff)
        self._order = ngram
        return result

    def score(self, words: Iterable[Word]) -> float:
        words = tuple(words)
        len_ = len(words)
        if len_ > self._order:
            raise NgramError(Word.to_str(words))

        if len_ == 1 and (words not in self._dic.keys()):
            raise NgramError(str(words) + 'は使用言語モデルの語彙にない')

        if words in self._dic.keys():
            return self._dic[words].prob
        else:
            context = words[:-1]
            p = self.score(words[1:])

            if context in self._dic.keys():
                backoff = self._dic[context].backoff
                return backoff + p
            else:
                return p

    def get_vocab(self) -> Set[Word]:
        return set(chain.from_iterable(self._dic.keys()))
