from typing import Union

from dataclasses import dataclass


@dataclass(init=True, repr=True, eq=True, frozen=True)
class YomiProperty:
    col: int
    pos: str


# ColNum = NewType('ColNum', int)
class ColNum(int):
    def __new__(klass, arg: Union[YomiProperty, int]) -> 'ColNum':
        if isinstance(arg, int):
            return super().__new__(klass, arg)  # type: ignore
        elif isinstance(arg, YomiProperty):
            return super().__new__(klass, arg.col)  # type: ignore
        else:
            raise TypeError()


# Position = NewType('Position', str)
class Position(str):
    def __new__(klass, yomi_prop: YomiProperty) -> 'Position':
        return super().__new__(klass, yomi_prop.pos)  # type: ignore
