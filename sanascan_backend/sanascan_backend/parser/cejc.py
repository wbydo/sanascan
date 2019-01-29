from typing import ClassVar, List, Tuple
from dataclasses import dataclass

import pandas as pd

from wbydo_parser.base import Parser, Result, ParseError
from wbydo_parser.multi import OneOrMore


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


class Sentence(Parser[Tuple[pd.Series, ...], pd.DataFrame]):
    def __call__(
            self,
            input: pd.DataFrame
            ) -> Result[Tuple[pd.Series, ...], pd.DataFrame]:

        sos_parser = SOS()
        sos_result = sos_parser(input)

        other_parser = OneOrMore(NotSOS())
        other_result = other_parser(sos_result.next)

        return Result(
            value=(sos_result.value, *other_result.value),
            next=other_result.next
        )
