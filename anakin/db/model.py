from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import relationship

from anakin.db.session import ENGINE

Base = automap_base()

class File(Base):
    __tablename__ = 'files'

    posts = relationship('Post')

    def __repr__(self):
        return "<File(id='{}', name='{}')".format(
            self.id,
            self.name
        )

class Post(Base):
    __tablename__ = 'posts'

    posts = relationship('Sentence')

    def __repr__(self):
        return "<Post(id={}, contents='{:<10}', file_id={})".format(
            self.id,
            self.contents,
            self.file_id
        )

class Sentence(Base):
    __tablename__ = 'sentences'

    def __repr__(self):
        return "<Post(id={}, contents='{:<10}', file_id={})".format(
            self.id,
            self.contents,
            self.file_id
        )

Base.prepare(ENGINE, reflect=True)
