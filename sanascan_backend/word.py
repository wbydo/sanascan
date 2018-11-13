from typing import NamedTuple, Dict, List

DELIMITER: str = '/'
MARK: Dict[str, str] = {
    'unk': '<unk>',
    'eng': '<eng>',
    'num': '<num>',
    '<s>': '<s>',  # 要検討
}


class Word(NamedTuple):
    surface: str
    yomi: str

    @staticmethod
    def from_str_of_multiword(sentence: str) -> 'List[Word]':
        return [Word.from_str_of_singleword(w) for w in sentence.split(' ')]

    @staticmethod
    def from_str_of_singleword(arg: str) -> 'Word':
        if arg in MARK.values():
            return Word(surface=arg, yomi=arg)

        list_ = arg.split(DELIMITER)
        if len(list_) >= 3:
            raise ValueError

        return Word(surface=list_[0], yomi=list_[1])

    @staticmethod
    def to_str(words: 'List[Word]') -> str:
        return ' '.join([str(w) for w in words])

    def __str__(self) -> str:
        if self.surface in MARK.values():
            return self.surface
        return f'{self.surface}{DELIMITER}{self.yomi}'

    def __repr__(self) -> str:
        return f'Word(\'{self.surface}\',\'{self.yomi}\')'
