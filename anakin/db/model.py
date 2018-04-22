from sqlalchemy import Column

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from anakin.db.session import ENGINE
from anakin.preprocess.dataset import Dataset

Base = automap_base()

class File(Base):
    __tablename__ = 'files'

    dataset = Column('dataset', Enum(Dataset))

    datum = relationship('Data')

    def __repr__(self):
        return "<File(id='{}', dataset='{}', file_name='{}')".format(
            self.id,
            self.dataset,
            self.file_name
        )

class Data(Base):
    __tablename__ = 'datum'

    sentences = relationship('Sentence')

    def __repr__(self):
        return "<Data(id={}, contents='{:<10}', file_id={})".format(
            self.id,
            self.contents,
            self.file_id
        )

class Sentence(Base):
    __tablename__ = 'sentences'

    lang_model_files = relationship('LangModelFile', secondary='created_lang_model')

    def __repr__(self):
        return "<Sentence(id={}, contents='{:<10}')".format(
            self.id,
            self.contents,
        )

class LangModelFile(Base):
    __tablename__ = 'lang_model_files'

    sentences = relationship('Sentence', secondary='created_lang_model')

Base.prepare(ENGINE, reflect=True)
