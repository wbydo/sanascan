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

    def _set_parent(self, parent: 'Node', order: int) -> None:
        self._parent = parent

        if parent.sentence is None:
            raise ValueError('parent.sentence is None')
        self.sentence = parent.sentence + [self._word]

        if len(parent.sentence) < order:
            self.sentence = parent.sentence + [self._word]
        else:
            self.sentence = parent.sentence[1:] + [self._word]

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
        if other.sentence is None:
            raise ValueError('other.sentence is None')

        if len(other.sentence) < order:
            ngram = other.sentence + [self._word]
        else:
            ngram = other.sentence[1:] + [self._word]

        # TODO: loggerにするor消すを検討
        print(ngram)
        return other.score + lang_model.score(ngram)

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
        self._set_parent(parent, order)


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
