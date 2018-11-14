from typing import List, Iterable

from .word import Word
from .lang_model import LangModel
from .key_to_word_map import KeyToWordMap
from .key import Key
from .node import Node, RootNode, EOSNode


def estimate(
        words: Iterable[Word],
        lang_model: LangModel,
        ) -> List[Word]:

    key = Key.from_words(list(words))

    root_node = RootNode()

    len_ = len(key)
    wait_child: List[List[Node]] = [[] for i in range(len_+1)]
    wait_child[0].append(root_node)

    key_to_word = KeyToWordMap(lang_model.get_vocab())

    for i in range(len_):
        if len(wait_child[i]) == 0:
            continue

        candidates = wait_child[i]
        for word, subkey in key_to_word.get_by_key(key, i):
            node = Node(word, candidates, lang_model)

            j = len(subkey) + i
            wait_child[j].append(node)

    eos_node = EOSNode(wait_child[len_], lang_model)

    if eos_node.sentence is None:
        raise Exception('eos_node.sentence is None')

    return eos_node.sentence[1:-1]
