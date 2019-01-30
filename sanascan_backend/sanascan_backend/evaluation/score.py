from dataclasses import dataclass


@dataclass(init=True, repr=True, eq=True, frozen=True)
class Score:
    correct: int = 0
    insert: int = 0
    substitute: int = 0
    dropout: int = 0

    def __add__(self, other: 'Score') -> 'Score':
        return Score(
            correct=self.correct + other.correct,
            insert=self.insert + other.insert,
            substitute=self.substitute + other.substitute,
            dropout=self.dropout + other.dropout
        )

    def __int__(self) -> int:
        penalty = self.insert + self.substitute + self.dropout
        return self.correct - (penalty)
