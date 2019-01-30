from dataclasses import dataclass
from functools import total_ordering


@dataclass(init=True, repr=True, eq=False, order=False, frozen=True)
@total_ordering
class Score:
    correct: int = 0
    insert: int = 0
    substitute: int = 0
    dropout: int = 0

    def __int__(self) -> int:
        cost = self.insert + self.substitute + self.dropout
        return self.correct - cost

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Score):
            return NotImplemented
        return int(self) == int(other)

    def __lt__(self, other: 'Score') -> bool:
        return int(self) < int(other)

    def __add__(self, other: 'Score') -> 'Score':
        return Score(
            correct=self.correct + other.correct,
            insert=self.insert + other.insert,
            substitute=self.substitute + other.substitute,
            dropout=self.dropout + other.dropout
        )
