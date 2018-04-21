from sqlalchemy.orm import relationship

from anakin.db.session import ENGINE
from anakin.db.base import Base

class Post(Base):
    __tablename__ = 'posts'

    posts = relationship('Sentence')

    def __repr__(self):
        return "<Post(id={}, contents='{:<10}', file_id={})".format(
            self.id,
            self.contents,
            self.file_id
        )

Base.prepare(ENGINE, reflect=True)
