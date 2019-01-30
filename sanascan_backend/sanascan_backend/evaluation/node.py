from typing import TYPE_CHECKING, Optional, Tuple, Iterable

from .score import Score
from ..word import Word

if TYPE_CHECKING:
    from .dp_matching import DPMatching


class IllegalAlgorithmError(Exception):
    pass


class Node:
    _x: int
    _y: int
    _matching_score: Score
    _dpm: 'DPMatching'

    is_root: bool
    parent: Optional['Node']
    score: Optional[Score]

    def __init__(
            self,
            x: int,
            y: int,
            ref: Word,
            est: Word,
            dpm: 'DPMatching',
            root: bool = False) -> None:

        self._x = x
        self._y = y
        self._matching_score = self._calc_matching_score(ref, est)
        self._dpm = dpm  # いらないかも？

        self.is_root = root
        self.parent = None
        self.score = None

        if self.is_root:
            self.score = self._matching_score
        else:
            self._set_parent()

    def position(self) -> Tuple[int, int]:
        return self._x, self._y

    def _is_match(self) -> bool:
        ms = self._matching_score
        if ms.perfect == 1 or ms.yomi == 1:
            return True
        return False

    def _parent_candidates(self) -> Iterable['Node']:
        # 局所的制約に関する処理
        if self._x >= 1 and self._y >= 1:
            yield self._dpm.get_node(self._x-1, self._y-1)
        if self._x >= 1:
            yield self._dpm.get_node(self._x-1, self._y)
        if self._y >= 1:
            yield self._dpm.get_node(self._x, self._y-1)

    def _calc_matching_score(self, ref: Word, est: Word) -> Score:
        # 重み関数に関する処理 1/2
        if ref == est:
            return Score(perfect=1)
        if ref.yomi == est.yomi:
            return Score(yomi=1)
        return Score()

    def _calc_score(self, other: 'Node') -> Score:
        # 重み関数に関する処理 2/2
        if (other._x == self._x - 1) and (other._y == self._y - 1):
            penalty = Score()
        else:
            if self._is_match() or other._is_match():
                penalty = Score(ignore=True)
            else:
                penalty = Score(miss=-1)

        assert other.score is not None
        return other.score + self._matching_score + penalty

    def _set_parent(self) -> None:
        parent = None
        max_score = Score()
        for can in self._parent_candidates():
            score = self._calc_score(can)

            if score >= max_score:
                parent = can
                max_score = score

        self.score = max_score
        self.parent = parent
