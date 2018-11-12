from typing import NamedTuple, Dict, List
from typing import ClassVar

class Word(NamedTuple):
    surface: str
    yomi: str

    DELIMITER: ClassVar[str] = '/'
    MARK: Dict[str, str] = {'unk':'<unk>', 'eng':'<eng>', 'num':'<num>'}

    @staticmethod
    def from_sentence(sentence: str) -> List[Word]:
        return [Word.from_str(w) for w in sentence.split(' ')]

    @staticmethod
    def from_str(str_: str) -> Word:
        if str_ in Word.MARK.values():
            return Word(surface=str_, yomi=str_)

        list_ = str_.split(Word.DELIMITER)
        if len(list_) >= 3:
            raise ValueError

        return Word(surface=list_[0], yomi=list_[1])

    def __str__(self) -> str:
        if self.surface in Word.MARK.values():
            return self.surface
        return f'{self.surface}{Word.DELIMITER}{self.yomi}'

    def __repr__(self) -> str:
        return f'Word(\'{self.surface}\',\'{self.yomi}\')'
