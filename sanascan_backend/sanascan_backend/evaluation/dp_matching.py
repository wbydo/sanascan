from typing import List, Dict, Tuple, Optional, Iterable

from .node import Node
from .score import Score

from ..word import Word


class DPMatching:
    _max_x: int
    _max_y: int

    _ref_words: List[Word]
    _est_words: List[Word]

    _nodes: Dict[Tuple[int, int], Node]
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

        self.end_node = self.get_node(self._max_x, self._max_y)
        self.score = self.end_node.score

    def get_node(self, x: int, y: int) -> Node:
        if x > self._max_x or y > self._max_y:
            raise ValueError()

        pos = (x, y)
        if pos in self._nodes:
            return self._nodes[pos]

        is_root = True if x == 0 and y == 0 else False
        node = Node(
            x=pos[0],
            y=pos[1],
            ref=self._ref_words[x],
            est=self._est_words[y],
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
