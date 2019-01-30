from typing import Iterable

from .node import Position

from ..word import Sentence


# ref / x 横軸
# est / y 縦軸


class DPMatching:
    ref_max: int
    est_max: int

    def __init__(self, ref: Sentence, est: Sentence) -> None:
        self.ref_max: int = len(ref.words) - 1
        self.est_max: int = len(est.words) - 1

        pos = Position(ref=self.ref_max, est=self.est_max)

        end_node = Node(
            position=pos,
            ref=ref.words[pos.ref],
            est=est.words[pos.est],
        )

    def _parent_position(self, pos: Position) -> Iterable[Position]:
        if (pos.ref - 1) >= 0 and (pos.est - 1) >= 0:
            yield Position(
                ref=pos.ref - 1,
                est=pos.est - 1,
            )

        if (pos.ref - 2) >= 0 and (pos.est - 1) >= 0:
            yield Position(
                ref=pos.ref - 2,
                est=pos.est - 1,
            )

        if (pos.ref - 1) >= 0 and (pos.est - 2) >= 0:
            yield Position(
                ref=pos.ref - 1,
                est=pos.est - 2,
            )
