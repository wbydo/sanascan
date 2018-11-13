from typing import Union, List, Optional

from .lang_model import LangModel
from .word import Word


class Node:
    _word: Union[Word, str]

    score: Optional[float]
    parent: 'Optional[Node]'
    sentence: Optional[str]
    sentence_clean: Optional[str]

    def __init__(self, word: Union[Word, str]) -> None:
        self._word = word

    def _set_score(self, score: float) -> None:
        self.score = score

    def _set_parent(self, parent: 'Node') -> None:
        if parent.sentence is None:
            raise ValueError('parent.sentence is None')
        if parent.sentence_clean is None:
            raise ValueError('parent.sentence_clean is None')

        self._parent = parent
        self.sentence = parent.sentence + ' ' + str(self._word)

        last: str
        if isinstance(self._word, str):
            last = self._word
        else:
            last = self._word.surface
        self.sentence_clean = parent.sentence_clean + ' ' + last

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

    def _pick_up_by_order(self, words: str, order: int) -> str:
        words_list = words.split(' ')
        if len(words_list) <= order:
            return words

        else:
            return ' '.join(words_list[-order:])

    def _calc_score(
            self,
            other: 'Node',
            lang_model: LangModel,
            order: int
            ) -> float:

        if other.sentence is None:
            raise ValueError('other.sentence is None')
        if other.score is None:
            raise ValueError('other.score is None')

        sentence = other.sentence + ' ' + str(self._word)
        words = Word.from_str_of_multiword(
            self._pick_up_by_order(sentence, order)
        )
        score = other.score + lang_model.score(words)

        return score


class RootNode(Node):
    def __init__(self) -> None:
        self._word = Word(surface='<s>', yomi='<s>')
        self.sentence = '<s>'
        self.sentence_clean = '<s>'
        self.score = 0.0


class EOSNode(Node):
    def __init__(self) -> None:
        self._word = Word(surface='</s>', yomi='</s>')
