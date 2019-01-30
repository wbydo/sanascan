from typing import TYPE_CHECKING, Optional, Iterable

from dataclasses import dataclass, replace, field

from .score import Score

if TYPE_CHECKING:
    from .dp_matching import DPMatching


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Position:
    ref: int
    est: int

    def parent_positions(self) -> Iterable['Position']:
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

    def is_root(self) -> bool:
        return self.ref == 0 and self.est == 0


@dataclass(init=True, repr=False, eq=False, frozen=False)
class Node:
    _pos: Position
    _dpm: 'DPMatching'

    parent: Optional['Node'] = field(init=False)
    score: Optional[Score] = field(init=False)

    def __post_init__(self) -> None:
        if self.is_root():
            self.score = self._calc_matching_score()
            self.parent = None
        else:
            parent = None
            max_score = Score()
            for can in self._parent_candidates():
                score = self._calc_score(can)

                if int(score) >= int(max_score):
                    parent = can
                    max_score = score

            self.score = max_score
            self.parent = parent

    def _parent_candidates(self) -> Iterable['Node']:
        for pos in self._pos.parent_positions():
            yield self._dpm.get_node(pos)

    def _calc_matching_score(self) -> Score:
        if self._dpm.is_match(self._pos):
            return Score(correct=1)
        else:
            return Score(substitute=1)

    def _calc_score(self, other: 'Node') -> Score:
        penalty = self._pos.penalty(other._pos)

        assert other.score is not None
        return other.score + self._calc_matching_score() + penalty

    def is_root(self) -> bool:
        return self._pos.is_root()
