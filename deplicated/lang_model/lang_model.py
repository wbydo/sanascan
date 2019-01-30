import re
from collections import namedtuple

from enum import Enum
from enum import auto

class ArpaArea(Enum):
        DATA = auto()
        NGRAM = auto()

class NgramError(Exception):
        pass

class LangModel:
        Data = namedtuple('Data', ['prob', 'backoff'])

        remove_head = re.compile(r'^(?:.*?) (?P<target>.*)$')
        remove_tail = re.compile(r'^(?P<target>.*) (?:.*?)$')

        def __init__(self, arpa_text):
                self._dic = self._process_arpa_file(arpa_text)
                self._keys = self._dic.keys()

        def _process_arpa_file(self, arpa_text):
                title = re.compile(r'^\\(\d)-grams:$')
                area = ArpaArea.DATA
                n_gram = None

                result = {}
                for unstriped_line in arpa_text.split('\n'):
                        line = unstriped_line.strip()
                        m = title.match(line)
                        if m:
                                area = ArpaArea.NGRAM
                                ngram = int(m.group(1))
                                continue

                        if area == ArpaArea.DATA or line == '' or line == '\\end\\':
                                continue

                        data_line = line.split('\t')
                        prob = float(data_line[0])
                        word = data_line[1]
                        backoff = float(data_line[2]) if len(data_line) == 3 else None
                        result[word] = LangModel.Data(prob=prob, backoff=backoff)
                self._order = ngram
                return result

        def _split(self, words):
                return words.split(' ')

        def _join(self, words):
                return ' '.join(words)

        def _remove_head(self, words):
                return LangModel.remove_head.search(words)['target']

        def _remove_tail(self, words):
                m = LangModel.remove_tail.search(words)
                return m['target']

        def score(self, words_arg):
                words = self._split(words_arg)
                l = len(words)
                if l > self._order:
                        raise NgramError(words_arg)

                if words_arg in self._keys:
                        return self._dic[words_arg].prob
                else:
                        preceed = self._remove_tail(words_arg)
                        reduced = self._remove_head(words_arg)
                        p = self.score(reduced)

                        #and以下のもの付けたけどいいんかこれ
                        if preceed in self._keys and self._dic[preceed].backoff:
                                return self._dic[preceed].backoff + p
                        else:
                                return p
