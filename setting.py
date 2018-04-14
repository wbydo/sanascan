from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import pymysql

import env

pymysql.install_as_MySQLdb()
Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    posts = relationship('Post')

    def __repr__(self):
        return "<File(id='{}', name='{}')".format(
            self.id,
            self.name
        )

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    contents = Column(Text)
    file_id = Column(
        Integer,
        ForeignKey('files.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
    UniqueConstraint('id', 'file_id')

    def __repr__(self):
        return "<Post(id={}, contents='{:<10}', file_id={})".format(
            self.id,
            self.contents,
            self.file_id
        )

DATABASE = 'mysql://{}:{}@{}/{}?charset=utf8'.format(
    env.USER_NAME,
    env.PASSWORD,
    env.HOST_IP,
    env.DB_NAME
)
ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True
)

# Base.metadata.drop_all(ENGINE)
Base.metadata.create_all(ENGINE)
