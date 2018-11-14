from typing import List

from .lang_model import LangModel
from .word import Word, TagWord


class Node:
    _word: Word
    score: float
    parent: 'Node'
    sentence: List[Word]

    def __init__(
            self,
            word: Word,
            candidates: 'List[Node]',
            lang_model: LangModel,
            ) -> None:

        self._word = word

        f = self._calc_score
        scores = [f(can, lang_model) for can in candidates]

        max_score = max(scores)
        self.score = max_score
        self.parent = candidates[scores.index(max_score)]
        self.sentence = self.parent.sentence + [self._word]

    def _calc_score(self, other: 'Node', lm: LangModel) -> float:
        ngram = other.sentence[-(lm.order - 1):] + [self._word]
        return other.score + lm.score(ngram)


class RootNode(Node):
    def __init__(self) -> None:
        word = TagWord('<s>')
        self._word = word
        self.sentence = [word]
        self.score = 0.0


class EOSNode(Node):
    def __init__(
            self, candidates: 'List[Node]',
            lang_model: LangModel) -> None:

        super(self.__class__, self).__init__(
            TagWord('</s>'),
            candidates,
            lang_model
        )
