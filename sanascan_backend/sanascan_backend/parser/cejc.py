import pandas as pd

from wbydo_parser.base import Parser, Result, ParseError


class SOS(Parser[pd.Series, pd.DataFrame]):
    def __call__(self, input: pd.DataFrame) -> Result[pd.Series, pd.DataFrame]:
        flag = input.iloc[0, :]['文頭フラグ']
        if flag == 'B':
            value = input.iloc[0, :]
            next_ = input.iloc[1:, :]
            return Result(value=value, next=next_)
        elif flag == 'I':
            raise ParseError(next=input)
        else:
            raise Exception()
