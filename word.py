from collections import namedtuple

class Word(namedtuple('Word', ['surface', 'yomi'])):
  DELIMITER = '/'
  MARK = {'unk':'<unk>', 'eng':'<eng>', 'num':'<num>'}

  @staticmethod
  def from_str(str_):
    if str_ in Word.MARK.values():
        return Word(surface=str_, yomi=str_)

    list_ = str_.split(Word.DELIMITER)
    if len(list_) >= 3:
      raise ValueError

    return Word(surface=list_[0], yomi=list_[1])

  def __str__(self):
    if self.surface in Word.MARK.values():
        return self.surface
    return f'{self.surface}{Word.DELIMITER}{self.yomi}'

  def __repr__(self):
    return f'Word(\'{self.surface}\',\'{self.yomi}\')'
