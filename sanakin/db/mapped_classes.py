from sqlalchemy import Column

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

Base = automap_base()

class Corpus(Base):
    __tablename__ = 'corpora'
    files = relationship('SKNFile')

class SKNFile(Base):
    __tablename__ = 'snkfiles'
    files = relationship('OriginalData')

class OriginalData(Base):
    __tablename__ = 'original_datum'
    sentences = relationship('Sentence')

class Sentence(Base):
    __tablename__ = 'sentences'

class SplitMethod(Base):
    __tablename__ = 'split_methods'
    sentences = relationship('Sentence')
