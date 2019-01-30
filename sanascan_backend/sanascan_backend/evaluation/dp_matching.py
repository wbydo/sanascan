from typing import List, Dict, Optional, Iterable

from .node import Node, Position
from .score import Score

from ..word import Word


class DPMatching:
    _max_ref: int
    _max_est: int

    _ref: List[Word]
    _est: List[Word]

    _nodes: Dict[Position, Node]
    end_node: Node
    score: Optional[Score]

    def __init__(
            self,
            ref_words: List[Word],
            est_words: List[Word]) -> None:

        self._max_ref = len(ref_words) - 1
        self._max_est = len(est_words) - 1

        self._ref = ref_words
        self._est = est_words

        self._nodes = {}

        pos = Position(ref=self._max_ref, est=self._max_est)
        self.end_node = self.get_node(pos)
        self.score = self.end_node.score

    def get_node(self, pos: Position) -> Node:
        if pos in self._nodes:
            return self._nodes[pos]

        node = Node(
            _pos=pos,
            _dpm=self,
        )
        self._nodes[pos] = node
        return node

    def nodes(self) -> Iterable[Node]:
        e = self.end_node
        while(not e.is_root):
            yield e
            assert e.parent is not None
            e = e.parent
        yield e

    def is_match(self, pos: Position) -> bool:
        # 読みだけで正解とするときはここを弄る
        ref: Word = self._ref[pos.ref]
        est: Word = self._est[pos.est]
        return ref == est
