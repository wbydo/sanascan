from typing import List, Iterable

from .word import Word
from .lang_model import LangModel
from .vocabulary import Vocabulary
from .key import Key
from .node import Node, RootNode, EOSNode


def estimate(
        words: Iterable[Word],
        lang_model: LangModel,
        ) -> List[Word]:

    key = Key.from_words(list(words))

    root_node = RootNode()

    key_len = len(key)
    wait_child: List[List[Node]] = [[] for i in range(key_len+1)]
    wait_child[0].append(root_node)

    vocab = Vocabulary(lang_model.get_vocab())

    for i in range(key_len):
        for word, subkey in vocab.get_by_key(key, i):
            subkey_len = len(subkey)

            candidates_idx = i - subkey_len + 1
            assert candidates_idx >= 0, f'i: {i}, subky: {subkey}'
            candidates = wait_child[candidates_idx]

            node = Node(word, candidates, lang_model)

            wait_child[i+1].append(node)

    eos_node = EOSNode(wait_child[-1], lang_model)

    if eos_node.sentence is None:
        raise Exception('eos_node.sentence is None')

    return eos_node.sentence[1:-1]
