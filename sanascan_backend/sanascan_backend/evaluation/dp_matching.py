from typing import List, Dict, Optional, Iterable

from .node import Node, Position
from .score import Score

from ..word import Word


class DPMatching:
    _max_x: int
    _max_y: int

    _ref_words: List[Word]
    _est_words: List[Word]

    _nodes: Dict[Position, Node]
    end_node: Node
    score: Optional[Score]

    def __init__(
            self,
            ref_words: List[Word],
            est_words: List[Word]) -> None:

        self._max_x = len(ref_words) - 1
        self._max_y = len(est_words) - 1

        self._ref_words = ref_words
        self._est_words = est_words

        self._nodes = {}

        pos = Position(self._max_x, self._max_y)
        self.end_node = self.get_node(pos)
        self.score = self.end_node.score

    def get_node(self, pos: Position) -> Node:
        if pos.ref > self._max_x or pos.est > self._max_y:
            raise ValueError()

        if pos in self._nodes:
            return self._nodes[pos]

        is_root = True if pos.ref == 0 and pos.est == 0 else False
        node = Node(
            pos,
            ref=self._ref_words[pos.ref],
            est=self._est_words[pos.est],
            dpm=self,
            root=is_root
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
