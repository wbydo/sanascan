from sqlalchemy.orm import relationship

from anakin.db.session import ENGINE
from anakin.db.base import Base

class File(Base):
    __tablename__ = 'files'

    posts = relationship('Post')

    def __repr__(self):
        return "<File(id='{}', name='{}')".format(
            self.id,
            self.name
        )

Base.prepare(ENGINE, reflect=True)
