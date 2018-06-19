from sqlalchemy import Column

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

Base = automap_base()

class Corpus(Base):
    __tablename__ = 'corpora'

    files = relationship('File')

class File(Base):
    __tablename__ = 'files'

    files = relationship('OriginalData')

class OriginalData(Base):
    __tablename__ = 'original_datum'
    sentences = relationship('Sentence')

class Sentence(Base):
    __tablename__ = 'sentences'


class SplitMethod(Base):
    __tablename__ = 'split_methods'
    sentences = relationship('Sentence')
# importしたら以下を実行
# Base.prepare(ENGINE, reflect=True)
