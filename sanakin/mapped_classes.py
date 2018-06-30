import os

from sqlalchemy import Column

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from .corpus_file import BaseCorpusFile
from .corpus import BaseCorpus

Base = automap_base()

class Corpus(Base, BaseCorpus):
    __tablename__ = 'corpora'
    corpus_files = relationship('CorpusFile')

    def extract_data(self, line):
        func = self._extract_function(self.corpus_id)
        return func(line)

class CorpusFile(Base, BaseCorpusFile):
    __tablename__ = 'corpus_files'
    origin_datum = relationship('CorpusData')

    def readline(self, dir_):
        file_path_ = os.path.join(dir_, self.corpus_file_id)
        for line in self._readline(file_path_):
            yield line

class CorpusData(Base):
    __tablename__ = 'corpus_datum'
    # sentences = relationship('Sentence')

class SentenceDelimiter(Base):
    __tablename__ = 'sentence_delimiters'

# class Sentence(Base):
#     __tablename__ = 'sentences'
#
# class SplitMethod(Base):
#     __tablename__ = 'split_methods'
#     sentences = relationship('Sentence')
