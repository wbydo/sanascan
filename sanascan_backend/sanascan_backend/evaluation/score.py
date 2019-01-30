from functools import total_ordering


@total_ordering
class Score:
    perfect: int
    yomi: int
    miss: int
    ignore: bool

    def __init__(
            self,
            perfect: int = 0,
            yomi: int = 0,
            miss: int = 0,
            ignore: bool = False) -> None:

        self.perfect = perfect
        self.yomi = yomi
        self.miss = miss
        self.ignore = ignore

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Score):
            return NotImplemented

        if not self.perfect == other.perfect:
            return False
        if not self.yomi == other.yomi:
            return False
        if not self.miss == other.miss:
            return False
        if not self.ignore == other.ignore:
            return False
        return True

    def __hash__(self) -> int:
        return hash((self.perfect, self.yomi, self.miss, self.ignore))

    def __lt__(self, other: 'Score') -> bool:
        # この条件だとother.ignore == Trueでもselfが小さいことになる
        # そんなに影響ないのでこうしておく
        if self.ignore:
            return True

        if self.perfect < other.perfect:
            return True

        if self.perfect == other.perfect\
            and self.yomi < other.yomi:
            return True

        if self.perfect == other.perfect\
            and self.yomi == other.yomi\
            and self.miss < other.miss:
            return True

        return False

    def __add__(self, other: 'Score') -> 'Score':
        return Score(
            perfect=self.perfect + other.perfect,
            yomi=self.yomi + other.yomi,
            miss=self.miss + other.miss,
            ignore=self.ignore or other.ignore
        )
