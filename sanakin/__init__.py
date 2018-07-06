from sqlalchemy.orm import sessionmaker

from .mapped_classes import(
    Base,
    Corpus,
    CorpusFile,
    CorpusData,
    SentenceDelimiter,
    Sentence,
    Morpheme,
    MorphemeDict
)

_Session = sessionmaker()

class SNKSession():
    @staticmethod
    def configure(**kwargs):
        _Session.configure(**kwargs)

    def __init__(self):
        self._s = _Session()

    def __enter__(self):
        return self._s

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self._s.rollback()
        else:
            self._s.commit()

        # self._s.close()
        return False
