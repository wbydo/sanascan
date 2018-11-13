from typing import Tuple, Iterable


class Key():
    _tpl: Tuple[int, ...]

    def __init__(self, *args: int) -> None:
        if not all([isinstance(i, int) for i in args]):
            raise TypeError

        self._tpl = tuple(args)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Key):
            return NotImplemented
        return self._tpl == other._tpl

    def __hash__(self) -> int:
        return hash(self._tpl)

    def __repr__(self) -> str:
        return '<Key {}>'.format(repr(self._tpl))

    def subsequence(self, start: int) -> 'Iterable[Key]':
        if start >= len(self._tpl):
            raise ValueError

        len_ = len(self._tpl)
        for i in range(start+1, len_+1):
            subtpl = self._tpl[start:i]
            yield Key(*subtpl)

    def __len__(self) -> int:
        return len(self._tpl)
