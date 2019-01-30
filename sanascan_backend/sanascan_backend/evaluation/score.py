from functools import total_ordering


@total_ordering
class Score:
    def __init__(self, perfect=0, yomi=0, miss=0, ignore=False):
        self.perfect = perfect
        self.yomi = yomi
        self.miss = miss
        self.ignore = ignore

    def __repr__(self):
        return f'Score(perfect={self.perfect}, yomi={self.yomi}, miss={self.miss}, ignore={self.ignore})'

    def __eq__(self, other):
        if not self.perfect == other.perfect:
            return False
        if not self.yomi == other.yomi:
            return False
        if not self.miss == other.miss:
            return False
        if not self.ignore == other.ignore:
            return False
        return True

    def __hash__(self):
        return hash((self.perfect, self.yomi, self.miss, self.ignore))

    def __lt__(self, other):
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

    def __add__(self, other):
        return Score(
            perfect=self.perfect + other.perfect,
            yomi=self.yomi + other.yomi,
            miss=self.miss + other.miss,
            ignore=self.ignore or other.ignore
        )
