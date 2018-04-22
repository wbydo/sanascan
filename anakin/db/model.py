from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from anakin.db.session import ENGINE

Base = automap_base()

class Dataset(Base):
    __tablename__ = 'datasets'

    files = relationship('File')

    def __repr(self):
        return "<Dataset(id='{}', name='{}')>".format(
            self.id,
            self.name
        )

class File(Base):
    __tablename__ = 'files'

    posts = relationship('Post')

    def __repr__(self):
        return "<File(id='{}', dataset='{}', file_name='{}')".format(
            self.id,
            self.dataset.name,
            self.file_name
        )

class Post(Base):
    __tablename__ = 'posts'

    sentences = relationship('Sentence')

    def __repr__(self):
        return "<Post(id={}, contents='{:<10}', file_id={})".format(
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
