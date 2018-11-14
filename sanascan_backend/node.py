from typing import List, Optional

from .lang_model import LangModel
from .word import Word, TagWord


class NodeException(Exception):
    pass


class Node:
    _word: Word

    score: Optional[float]
    parent: 'Optional[Node]'
    sentence: Optional[List[Word]]

    def __init__(self, word: Word) -> None:
        self._word = word

    def _set_score(self, score: float) -> None:
        self.score = score

    def _set_parent(self, parent: 'Node') -> None:
        self._parent = parent

        if parent.sentence is None:
            raise ValueError('parent.sentence is None')

        self.sentence = parent.sentence + [self._word]

    def _calc_score(
            self,
            other: 'Node',
            lm: LangModel,
            ) -> float:

        if other.score is None:
            raise ValueError('other.score is None')
        if other.sentence is None:
            raise ValueError('other.sentence is None')

        ngram = other.sentence[-(lm.order - 1):] + [self._word]
        return other.score + lm.score(ngram)

    def search_parent(
            self,
            candidates: 'List[Node]',
            lang_model: LangModel,
            ) -> None:

        f = self._calc_score
        scores = [f(can, lang_model) for can in candidates]

        max_score = max(scores)
        self._set_score(max_score)

        parent = candidates[scores.index(max_score)]
        self._set_parent(parent)


class ConstantNode(Node):
    def _set_parent(self, parent: 'Node') -> None:
        raise NodeException()


class RootNode(ConstantNode):
    def __init__(self) -> None:
        word = TagWord('<s>')
        super(self.__class__, self).__init__(word)

        self.sentence = [word]
        self.score = 0.0


class EOSNode(Node):
    def __init__(self) -> None:
        word = TagWord('</s>')
        super(self.__class__, self).__init__(word)
