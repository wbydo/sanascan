from typing import List, ClassVar, Tuple, Iterable

from dataclasses import dataclass


class Word:
    surface: str
    yomi: str
    DELIMITER: ClassVar[str] = '/'

    @staticmethod
    def from_wakachigaki(wakachigaki: str) -> 'List[Word]':
        return [Word.from_str_of_singleword(w) for w in wakachigaki.split(' ')]

    @classmethod
    def from_str_of_singleword(klass, arg: str) -> 'Word':
        if TagWord.is_include(arg):
            return TagWord(arg)

        list_ = arg.split(klass.DELIMITER)

        if len(list_) >= 3:
            raise ValueError()

        return Word(surface=list_[0], yomi=list_[1])

    def __init__(self, surface: str, yomi: str) -> None:
        self.surface = surface
        self.yomi = yomi

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return NotImplemented

        klass = self.__class__
        if not isinstance(other, klass):
            return False
        return self.__tuple__() == other.__tuple__()

    def __hash__(self) -> int:
        return hash(self.__tuple__())

    def __tuple__(self) -> Tuple[str, str]:
        return (self.surface, self.yomi)

    def __str__(self) -> str:
        return f'{self.surface}{self.DELIMITER}{self.yomi}'

    def __repr__(self) -> str:
        return f'Word(\'{self.surface}\',\'{self.yomi}\')'


class TagWord(Word):
    _tags: ClassVar[List[str]] = ['<unk>', '<eng>', '<num>', '<s>', '</s>']

    @classmethod
    def is_include(klass, arg: str) -> bool:
        return arg in klass._tags

    def __init__(self, arg: str) -> None:
        if arg not in self._tags:
            raise ValueError(arg)
        super(self.__class__, self).__init__(surface=arg, yomi=arg)

    def __str__(self) -> str:
        return self.surface


@dataclass(init=True, repr=False, eq=True, frozen=True)
class Sentence:
    DELIMITER: ClassVar[str] = ' '
    words: Tuple[Word, ...]

    @classmethod
    def from_iter(klass, words: Iterable[Word]) -> 'Sentence':
        return klass(tuple(words))

    def __str__(self) -> str:
        return self.DELIMITER.join(
            [str(w) for w in self.words]
        )

    def format_surfaces(self) -> str:
        return ''.join(
            [w.surface for w in self.words]
        )
