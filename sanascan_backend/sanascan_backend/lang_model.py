import re
from typing import Dict, Set, Tuple, IO
from enum import Enum
from enum import auto
from itertools import chain

from .word import Word, Sentence
from .vocabulary import Vocabulary


class ArpaArea(Enum):
        DATA = auto()
        NGRAM = auto()


class NgramError(Exception):
    pass


class ParseError(Exception):
    pass


class LangModel:
    class Data:
        prob: float
        backoff: float

        def __init__(self, prob: float, backoff: float) -> None:
            self.prob = prob
            self.backoff = backoff

    _dic: Dict[Tuple[Word, ...], Data]
    order: int

    def __init__(self, arpa: IO[str]) -> None:
        title = re.compile(r'^\\(\d)-grams:$')
        area = ArpaArea.DATA

        result = {}
        for unstriped_line in iter(arpa.readline, ''):
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

        self.order = ngram
        self._dic = result

    def score(self, sentence: Sentence) -> float:
        len_ = len(sentence.words)
        if len_ > self.order:
            raise NgramError(sentence.format_surfaces())

        words = sentence.words
        if len_ == 1 and (words not in self._dic.keys()):
            raise NgramError(str(words) + 'は使用言語モデルの語彙にない')

        if words in self._dic.keys():
            return self._dic[words].prob
        else:
            context = words[:-1]
            s = Sentence.from_iter(words[1:])
            p = self.score(s)

            if context in self._dic.keys():
                backoff = self._dic[context].backoff
                return backoff + p
            else:
                return p

    def _get_word_set(self) -> Set[Word]:
        return set(chain.from_iterable(self._dic.keys()))

    def create_vocabrary(self) -> Vocabulary:
        return Vocabulary(self._get_word_set())
