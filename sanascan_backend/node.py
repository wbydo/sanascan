from typing import List, Optional

from .lang_model import LangModel
from .word import Word


class NodeException(Exception):
    pass


class Node:
    _word: Word

    score: Optional[float]
    parent: 'Optional[Node]'
    sentence: List[Word]

    def __init__(self, word: Word) -> None:
        self._word = word

    def _set_score(self, score: float) -> None:
        self.score = score

    def _set_parent(self, parent: 'Node') -> None:
        self._parent = parent
        self.sentence = parent.sentence + [self._word]

    def _pick_up_by_order(self, words: List[Word], order: int) -> List[Word]:
        if len(words) <= order:
            return words

        else:
            return words[-order:]

    def _calc_score(
            self,
            other: 'Node',
            lang_model: LangModel,
            order: int
            ) -> float:

        if other.score is None:
            raise ValueError('other.score is None')

        sentence = other.sentence + [self._word]
        score = other.score + lang_model.score(sentence)

        return score

    def search_parent(
            self,
            candidates: 'List[Node]',
            lang_model: LangModel,
            order: int
            ) -> None:

        f = self._calc_score
        scores = [f(can, lang_model, order) for can in candidates]

        max_score = max(scores)
        self._set_score(max_score)

        parent = candidates[scores.index(max_score)]
        self._set_parent(parent)


class ConstantNode(Node):
    def _set_parent(self, parent: 'Node') -> None:
        raise NodeException()


class RootNode(ConstantNode):
    def __init__(self) -> None:
        word = Word(surface='<s>', yomi='<s>')
        super(self.__class__, self).__init__(word)

        self.sentence = [word]
        self.score = 0.0


class EOSNode(Node):
    def __init__(self) -> None:
        self._word = Word(surface='</s>', yomi='</s>')
