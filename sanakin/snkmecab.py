import sys

from natto import MeCab

from .const import MAX_MECAB_PARSE_NUM

class SNKMeCab(MeCab):
    def __init__(self, options=None, **kw):
        self._options = options
        self._kw = kw

        super(self.__class__, self).__init__(options=self._options, **self._kw)
        self._count = 0

    def parse(self, text, **kw):
        if self._count >= MAX_MECAB_PARSE_NUM:
            self.__del__()
            super(self.__class__, self).__init__(options=self._options, **self._kw)

            self._count = 0

        self._count += 1
        return super(self.__class__, self).parse(text, **kw)
