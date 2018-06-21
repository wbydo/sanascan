from sqlalchemy import Column

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from . import snkfile
from . import corpus

Base = automap_base()

class Corpus(Base):
    __tablename__ = 'corpora'
    snkfiles = relationship('SNKFile')

    def extract_data(self, line):
        return corpus._extract_data(self.symbol)(line)

class SNKFile(Base):
    __tablename__ = 'snkfiles'
    origin_datum = relationship('OriginalData')

    def readline(self, dir_):
        for line in snkfile._readline(self, dir_):
            yield line

class OriginalData(Base):
    __tablename__ = 'original_datum'
    sentences = relationship('Sentence')

class Sentence(Base):
    __tablename__ = 'sentences'

class SplitMethod(Base):
    __tablename__ = 'split_methods'
    sentences = relationship('Sentence')
