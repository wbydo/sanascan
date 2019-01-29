from typing import Union

from dataclasses import dataclass


@dataclass(init=True, repr=True, eq=True, frozen=True)
class YomiProperty:
    col: int
    pos: str


class ColNum(int):
    @classmethod
    def create(klass, arg: Union[YomiProperty, int]) -> 'ColNum':
        if isinstance(arg, int):
            return klass(arg)
        elif isinstance(arg, YomiProperty):
            return klass(arg.col)
        else:
            raise TypeError()


class Position(str):
    @classmethod
    def create(klass, arg: Union[YomiProperty, str]) -> 'Position':
        if isinstance(arg, str):
            return klass(arg)
        elif isinstance(arg, YomiProperty):
            return klass(arg.pos)
        else:
            raise TypeError()
