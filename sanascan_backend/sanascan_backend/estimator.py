from typing import List, cast, Optional

from .word import Word, TagWord
from .lang_model import LangModel
from .key import Key
from .node import Node, RootNode, EOSNode
from .vocabulary import Vocabulary


class Estimator:
    lang_mode: LangModel
    vocab: Vocabulary
    wait_child: List[List[Node]]  # あとで変数名変えたい
    key: Key
    eos_node: Optional[EOSNode]
    result: Optional[List[Word]]

    def __init__(self, lm: LangModel) -> None:
        self.lang_model = lm
        self.vocab = lm.create_vocabrary()

        self.reset()

    def add(self, key: Key) -> None:
        assert len(key) == 1

        self.wait_child.append([])
        self.key += key

        for word, subkey in self.vocab.get_by_key(self.key):
            candidates_idx = len(self.key) - len(subkey) - 1
            assert candidates_idx >= 0
            candidates = self.wait_child[candidates_idx]
            node = Node(word, candidates, self.lang_model)
            self.wait_child[-1].append(node)

        scores = [node.score for node in self.wait_child[-1]]
        max_node = self.wait_child[-1][scores.index(max(scores))]
        self.result = max_node.sentence[1:]

    def finish(self) -> None:
        self.eos_node = EOSNode(self.wait_child[-1], self.lang_model)
        self.result = self.eos_node.sentence[1:-1]

    def reset(self) -> None:
        self.result = None
        self.wait_child = [[]]
        self.wait_child[0].append(RootNode())

        s_tag = cast(
            TagWord,
            self.wait_child[0][0]._word,
        )

        self.key = Key([s_tag])
