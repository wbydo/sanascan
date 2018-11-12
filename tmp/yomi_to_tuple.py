from enum import Enum
from enum import auto

from collections import namedtuple
from collections import defaultdict

from anakin.util.word import Word
from anakin.util.key import Key

katakana_table = [
    'アイウエオヴァィゥェォ',
    'カキクケコガギグゲゴ',
    'サシスセソザジズゼゾ',
    'タチツテトッダヂヅデド',
    'ナニヌネノ',
    'ハヒフヘホバビブベボパピプペポ',
    'マミムメモ',
    'ヤユヨャュョ',
    'ラリルレロ',
    'ワヲンー'
]

num_table = {c:idx for idx, col in enumerate(katakana_table) for c in col}

ResultOfGetByKey = namedtuple('ResultOfGetByKey', ['word', 'key'])

class SearchFlag(Enum):
    PROCEED = auto()
    STOP = auto()

class KeyToWord():
    def __init__(self, words):
        self._datum = {}
        self._search_map = defaultdict(
            lambda:SearchFlag.STOP)

        for word in words:
            key = Key(*yomi2tuple(word.yomi))

            self._add_data(key, word)

    def _add_data(self, key, word):
        if not (key in self._datum.keys()):
            self._datum[key] = []
        self._datum[key].append(word)

        for subkey in key.subsequence(0):
            self._search_map[subkey] = SearchFlag.PROCEED

    def get_by_key(self, key, start):
        if not isinstance(key, Key):
            raise TypeError

        for subkey in key.subsequence(start):
            if self._search_map[subkey] == SearchFlag.STOP:
                break
            if subkey in self._datum.keys():
                for word in self._datum[subkey]:
                    yield ResultOfGetByKey(word=word, key=subkey)

def yomi2tuple(yomi):
    if yomi in Word.MARK.values():
        return (yomi,)
    return tuple([num_table[i] for i in yomi])
