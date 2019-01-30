from typing import TYPE_CHECKING, Optional, Iterable

from dataclasses import dataclass, replace

from .score import Score
from ..word import Word

if TYPE_CHECKING:
    from .dp_matching import DPMatching


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Position:
    ref: int
    est: int

    def parent_candidates_positions(self) -> Iterable['Position']:
        if self.ref - 1 >= 0 and self.est - 1 >= 0:
            yield replace(self, ref=self.ref-1, est=self.est-1)
        if self.ref - 2 >= 0 and self.est - 1 >= 0:
            yield replace(self, ref=self.ref-2, est=self.est-1)
        if self.ref - 1 >= 0 and self.est - 2 >= 0:
            yield replace(self, ref=self.ref-1, est=self.est-2)

    def penalty(self, other: 'Position') -> Score:
        if (other.ref == self.ref - 1) and (other.est == self.est - 1):
            penalty = Score()
        elif (other.ref == self.ref - 2) and (other.est == self.est - 1):
            penalty = Score(dropout=1)
        elif (other.ref == self.ref - 1) and (other.est == self.est - 2):
            penalty = Score(insert=1)
        else:
            raise Exception()
        return penalty


class Node:
    _pos: Position
    _matching_score: Score
    _dpm: 'DPMatching'

    is_root: bool
    parent: Optional['Node']
    score: Optional[Score]

    def __init__(
            self,
            pos: Position,
            ref: Word,
            est: Word,
            dpm: 'DPMatching',
            root: bool = False) -> None:

        self._pos = pos
        self._matching_score = self._calc_matching_score(ref, est)
        self._dpm = dpm  # いらないかも？

        self.is_root = root
        self.parent = None
        self.score = None

        if self.is_root:
            self.score = self._matching_score
        else:
            self._set_parent()

    def _parent_candidates(self) -> Iterable['Node']:
        # 局所的制約に関する処理
        for pos in self._pos.parent_candidates_positions():
            yield self._dpm.get_node(pos)

    def _calc_matching_score(self, ref: Word, est: Word) -> Score:
        # 読みだけで正解とするときはここを弄る
        return Score(correct=1) if ref == est else Score(substitute=1)

    def _calc_score(self, other: 'Node') -> Score:
        penalty = self._pos.penalty(other._pos)

        assert other.score is not None
        return other.score + self._matching_score + penalty

    def _set_parent(self) -> None:
        parent = None
        max_score = Score()
        for can in self._parent_candidates():
            score = self._calc_score(can)

            if int(score) >= int(max_score):
                parent = can
                max_score = score

        self.score = max_score
        self.parent = parent
