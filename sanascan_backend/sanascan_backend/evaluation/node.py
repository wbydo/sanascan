from dataclasses import dataclass

from .score import Score
from ..word import Word


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Position:
    ref: int
    est: int


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Node:
    position: Position
    ref: Word
    est: Word
    score: Score
    parent: 'Node'
