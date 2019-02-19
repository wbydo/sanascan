from typing import ClassVar, List, Optional, Tuple
from dataclasses import dataclass

import pandas as pd

from wbydo_parser.base import Parser, Result, ParseError
from wbydo_parser.multi import ZeroOrMore, OneOrMore

from ..word import Word, Sentence
from ..word_builder import WordBuilder


class BuilderFromCEJC(WordBuilder):
    def __init__(self, row: pd.Series):
        self._hinshi = row['品詞'].split('-')[0]
        self._surface = row['書字形']

        yomi = row['語形']
        if isinstance(yomi, str) and len(yomi) != 0:
            self._has_yomi = True
        else:
            self._has_yomi = False

        if self._has_yomi:
            self._yomi = yomi


@dataclass(init=True, repr=True, eq=True, frozen=True)
class SentenceHeadFrag(Parser[Optional[Word], pd.DataFrame]):
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

    def __call__(
            self,
            input: pd.DataFrame
            ) -> Result[Optional[Word], pd.DataFrame]:

        if input.empty:
            raise ParseError(next=input, msg='DataFrame is Empty')

        flag = input.iloc[0, :]['文頭フラグ']
        if flag == self.flag:
            next_ = input.iloc[1:, :]

            row = input.iloc[0, :]
            word = BuilderFromCEJC(row).to_word()

            return Result(value=word, next=next_)
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


class SentenceParser(Parser[Sentence, pd.DataFrame]):
    def __call__(
            self,
            input: pd.DataFrame
            ) -> Result[Sentence, pd.DataFrame]:

        sos_parser = SOS()
        sos_result = sos_parser(input)

        other_parser = ZeroOrMore(NotSOS())
        other_result = other_parser(sos_result.next)

        tmp = [sos_result.value, *other_result.value]
        words = tuple(w for w in tmp if w is not None)
        value = Sentence(words=words)

        return Result(
            value=value,
            next=other_result.next
        )


class CEJC(Parser[Tuple[Sentence, ...], pd.DataFrame]):
    def __call__(
            self,
            input: pd.DataFrame
            ) -> Result[Tuple[Sentence, ...], pd.DataFrame]:

        parser = OneOrMore(SentenceParser())
        return parser(input)
