from sqlalchemy import Column

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from . import corpus_file
from . import corpus

Base = automap_base()

class Corpus(Base):
    __tablename__ = 'corpora'
    corpus_files = relationship('CorpusFile')

    def extract_data(self, line):
        return corpus._extract_data(self.corpus_id)(line)

class CorpusFile(Base):
    __tablename__ = 'corpus_files'
    origin_datum = relationship('CorpusData')

    def readline(self, dir_):
        for line in corpus_file._readline(self, dir_):
            yield line

class CorpusData(Base):
    __tablename__ = 'corpus_datum'
    # sentences = relationship('Sentence')

# class Sentence(Base):
#     __tablename__ = 'sentences'
#
# class SplitMethod(Base):
#     __tablename__ = 'split_methods'
#     sentences = relationship('Sentence')
