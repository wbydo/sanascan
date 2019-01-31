from typing import Dict

from dataclasses import dataclass, field

from .node import Node, Position
from .score import Score

from ..word import Word, Sentence


@dataclass(init=True, repr=True, eq=True, frozen=False)
class WordAccuracy:
    size: int
    score: Score
    accuracy: float = field(init=False)

    def __post_init__(self) -> None:
        self.accuracy = int(self.score) / self.size


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

    def get_accuracy(self) -> WordAccuracy:
        # __init__と同時に再帰的に求まっているはず
        assert self.end_node is not None
        assert self.end_node.score is not None

        return WordAccuracy(
            size=len(self._ref.words),
            score=self.end_node.score
        )
