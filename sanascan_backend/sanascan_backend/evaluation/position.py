from typing import Iterable

from dataclasses import dataclass, replace

from .score import Score


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
