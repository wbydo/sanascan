from typing import Dict

from dataclasses import dataclass, field

from .node import Node, Position

from ..word import Word, Sentence


@dataclass(init=True, repr=False, eq=False, frozen=False)
class DPMatching:
    _ref: Sentence
    _est: Sentence

    _nodes: Dict[Position, Node] = field(init=False)
    end_node: Node = field(init=False)

    def __post_init__(self) -> None:
        self._nodes = {}

        max_ref = len(self._ref.words) - 1
        max_est = len(self._est.words) - 1
        pos = Position(ref=max_ref, est=max_est)
        self.end_node = self.get_node(pos)

    def get_node(self, pos: Position) -> Node:
        if pos in self._nodes:
            return self._nodes[pos]

        node = Node(_pos=pos, _dpm=self)
        self._nodes[pos] = node
        return node

    def is_match(self, pos: Position) -> bool:
        # 読みだけで正解とするときはここを弄る
        ref: Word = self._ref.words[pos.ref]
        est: Word = self._est.words[pos.est]
        return ref == est
