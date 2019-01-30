from collections import namedtuple, defaultdict
from functools import total_ordering

class DPMatching:
    def __init__(self, ref_words, est_words):
        self._max_x = len(ref_words) - 1
        self._max_y = len(est_words) - 1

        self._ref_words = ref_words
        self._est_words = est_words

        self._nodes = {}

        self.end_node = self.get_node(self._max_x, self._max_y)
        self.score = self.end_node.score

    def get_node(self, x, y):
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

    def nodes(self):
        e = self.end_node
        while(not e.is_root):
            yield e
            e = e.parent
        yield e

class IllegalAlgorithmError(Exception):
    pass

class Node:
    def __init__(self, x, y, ref, est, dpm, root=False):
        self._x = x
        self._y = y
        self._matching_score = self._calc_matching_score(ref, est)
        self._dpm = dpm # いらないかも？

        self.is_root = root
        self.parent = None
        self.score = None

        if self.is_root:
            self.score = self._matching_score
        else:
            self._set_parent()

    def __repr__(self):
        return f'Node(x={self._x}, y={self._y})'

    def position(self):
        return self._x, self._y

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError()

        if self.is_root and other.is_root:
            return True

        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash(tuple(self))

    def __tuple__(self):
        if self.is_root:
            return self.position()

        if not self._parent:
            raise IllegalAlgorithmError('親ノードが決定していない')

        return self.position() + self._parent.position()

    def _is_match(self):
        ms = self._matching_score
        if ms.perfect == 1 or ms.yomi == 1:
            return True
        return False

    def _parent_candidates(self):
        # 局所的制約に関する処理
        if self._x >= 1 and self._y >= 1:
            yield self._dpm.get_node(self._x-1, self._y-1)
        if self._x >= 1:
            yield self._dpm.get_node(self._x-1, self._y)
        if self._y >= 1:
            yield self._dpm.get_node(self._x, self._y-1)

    def _prev_path(self):
        if not self.parent:
            raise IllegalAlgorithmError('親ノードが決定していない')

        return (
            self._x - self._parent._x,
            self._y - self._parent._y
        )

    def _calc_matching_score(self, ref, est):
        # 重み関数に関する処理 1/2
        if ref == est:
            return Score(perfect=1)
        if ref.yomi == est.yomi:
            return Score(yomi=1)
        return Score()

    def _calc_score(self, other):
        # 重み関数に関する処理 2/2
        if (other._x == self._x - 1) and (other._y == self._y - 1):
            penalty = Score()
        else:
            if self._is_match() or other._is_match():
                penalty = Score(ignore=True)
            else:
                penalty = Score(miss=-1)

        return other.score + self._matching_score + penalty

    def _set_parent(self):
        parent = None
        max_score = Score()
        for can in self._parent_candidates():
            score = self._calc_score(can)

            if score >= max_score:
                parent = can
                max_score = score

        self.score = max_score
        self.parent = parent
