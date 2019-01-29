from typing import ClassVar, List
from dataclasses import dataclass

import pandas as pd

from wbydo_parser.base import Parser, Result, ParseError


@dataclass(init=True, repr=True, eq=True, frozen=True)
class SentenceHeadFrag(Parser[pd.Series, pd.DataFrame]):
    flag: str
    candidate: ClassVar[List[str]] = ['B', 'I']

    def __post_init__(self) -> None:
        if self.flag not in self.candidate:
            raise ValueError()

    def _other_flag(self) -> str:
        candidate = self.candidate[:]
        i = candidate.index(self.flag)
        candidate.pop(i)
        return candidate[0]

    def __call__(self, input: pd.DataFrame) -> Result[pd.Series, pd.DataFrame]:
        flag = input.iloc[0, :]['文頭フラグ']
        if flag == self.flag:
            value = input.iloc[0, :]
            next_ = input.iloc[1:, :]
            return Result(value=value, next=next_)
        elif flag == self._other_flag():
            raise ParseError(next=input)
        else:
            raise Exception()


class SOS(SentenceHeadFrag):
    def __init__(self) -> None:
        super().__init__(flag='B')


class NotSOS(SentenceHeadFrag):
    def __init__(self) -> None:
        super().__init__(flag='I')
