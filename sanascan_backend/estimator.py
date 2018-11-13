from typing import Union, List, Iterable

from .word import Word
from .lang_model import LangModel
from .yomi_to_tuple import KeyToWord
from .yomi_to_tuple import yomi2tuple
from .key import Key


class Node:
    _word: Union[Word, str]
    score: float

    def __init__(self, word: Union[Word, str], root: bool = False) -> None:
        self._word = word
        if root:
            self._word = '<s>'
            self.sentence = '<s>'
            self.sentence_clean = '<s>'
            self.score = 0.0

    def _set_score(self, score: float) -> None:
        self.score = score

    def _set_parent(self, parent: 'Node') -> None:
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

        sentence = other.sentence + ' ' + str(self._word)
        words = Word.from_str_of_multiword(
            self._pick_up_by_order(sentence, order)
        )
        score = other.score + lang_model.score(words)

        return score


def estimate(
        words: Iterable[Word],
        key_to_word: KeyToWord,
        lang_model: LangModel,
        order: int
        ) -> List[Word]:

    t = sum((yomi2tuple(w.yomi) for w in words), ())
    key = Key(*t)

    root_node = Node('', root=True)

    len_ = len(key)
    wait_child: List[List[Node]] = [[] for i in range(len_+1)]
    wait_child[0].append(root_node)

    for i in range(len_):
        if len(wait_child[i]) == 0:
            continue

        candidates = wait_child[i]
        for word, subkey in key_to_word.get_by_key(key, i):
            node = Node(word)
            node.search_parent(candidates, lang_model, order)

            j = len(subkey) + i
            wait_child[j].append(node)

    eos_node = Node('</s>')
    eos_node.search_parent(wait_child[len_], lang_model, order)
    # return eos_node
    est_sentence = ' '.join(eos_node.sentence.split(' ')[1:-1])
    return Word.from_str_of_multiword(est_sentence)
