from sqlalchemy import create_engine, Column, Integer,\
    String, Text, ForeignKey, UniqueConstraint,\
    ForeignKeyConstraint, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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

created_lang_model_table = Table("created_lang_model", Base.metadata,
    Column("sentence_id", Integer, ForeignKey("sentences.id", onupdate='CASCADE', ondelete='CASCADE')),
    Column("lang_model_id", Integer, ForeignKey("lang_model_files.id", onupdate='CASCADE', ondelete='CASCADE')),
)

class Sentence(Base):
    __tablename__ = 'sentences'
    __table_args__ = (ForeignKeyConstraint(
        ['post_id','post_file_id'],
        ['posts.id', 'posts.file_id']
    ), {})


    id = Column(Integer, primary_key=True)
    contents = Column(Text)
    post_id = Column(
        Integer,
        ForeignKey('posts.id', onupdate='CASCADE', ondelete='CASCADE'),
    )
    post_file_id = Column(
        Integer,
        ForeignKey('posts.file_id', onupdate='CASCADE', ondelete='CASCADE'),
    )

    lang_models = relationship("LangModelFile", secondary=created_lang_model_table)

    def __repr__(self):
        return "<Sentence(id={}, contents='{}')".format(
            self.id,
            self.contents
        )

class LangModelFile(Base):
    __tablename__ = 'lang_model_files'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    order = Column(Integer)

    sentences = relationship("Sentence", secondary=created_lang_model_table)

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

Session = sessionmaker(bind=ENGINE)

# Base.metadata.drop_all(ENGINE)
Base.metadata.create_all(ENGINE)
