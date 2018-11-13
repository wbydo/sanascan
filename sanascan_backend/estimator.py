from typing import List, Iterable

from .word import Word
from .lang_model import LangModel
from .yomi_to_tuple import KeyToWord
from .yomi_to_tuple import yomi2tuple
from .key import Key
from .node import Node, RootNode, EOSNode


def estimate(
        words: Iterable[Word],
        key_to_word: KeyToWord,
        lang_model: LangModel,
        order: int
        ) -> List[Word]:

    t = sum((yomi2tuple(w.yomi) for w in words), ())
    key = Key(*t)

    root_node = RootNode()

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

    eos_node = EOSNode()
    eos_node.search_parent(wait_child[len_], lang_model, order)

    if eos_node.sentence is None:
        raise Exception('eos_node.sentence is None')

    return eos_node.sentence[1:-1]
