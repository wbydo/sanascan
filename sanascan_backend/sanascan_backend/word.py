from typing import List, ClassVar, Tuple, Iterable


DELIMITER: str = '/'
# MARK: Dict[str, str] = {
#     'unk': '<unk>',
#     'eng': '<eng>',
#     'num': '<num>',
#     '<s>': '<s>',  # 要検討
# }


class Word:
    surface: str
    yomi: str

    @staticmethod
    def from_wakachigaki(wakachigaki: str) -> 'List[Word]':
        return [Word.from_str_of_singleword(w) for w in wakachigaki.split(' ')]

    @staticmethod
    def from_str_of_singleword(arg: str) -> 'Word':
        if TagWord.is_include(arg):
            return TagWord(arg)

        list_ = arg.split(DELIMITER)

        if len(list_) >= 3:
            raise ValueError()

        return Word(surface=list_[0], yomi=list_[1])

    @staticmethod
    def to_str(words: 'Iterable[Word]') -> str:
        return ''.join([w.surface for w in words])

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
        return f'{self.surface}{DELIMITER}{self.yomi}'

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
