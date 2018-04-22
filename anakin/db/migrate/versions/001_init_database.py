from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, Text,
    ForeignKey,PrimaryKeyConstraint
)
from sqlalchemy.types import BINARY, Enum
from sqlalchemy.dialects.mysql import LONGBLOB

from migrate import *

from anakin.preprocess.dataset import Dataset

meta = MetaData()

file_table = Table(
    'files', meta,
    Column('id', Integer, primary_key=True),
    Column('dataset', Enum(Dataset)),
    Column('file_name', String(100), unique=True),
    Column('contents', LONGBLOB),
    Column('checksum', BINARY(255), unique=True)
)

data_table = Table(
    'datum', meta,
    Column('id', Integer),
    Column('contents', Text),
    Column(
        'file_id', Integer,
        ForeignKey('files.id', onupdate='CASCADE', ondelete='CASCADE'),
    ),
    PrimaryKeyConstraint('id', 'file_id')

)

sentence_table = Table(
    'sentences', meta,
    Column('id', Integer, primary_key=True),
    Column('contents', Text),
    Column('data_id', Integer),
    Column('data_file_id', Integer),

    ForeignKeyConstraint(
        ['data_id','data_file_id'],
        ['datum.id', 'datum.file_id']
    )
)

lang_model_file_table = Table(
    'lang_model_files', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), unique=True),
    Column('order', Integer)
)

created_lang_model_table = Table(
    "created_lang_model", meta,
    Column("sentence_id", Integer, ForeignKey("sentences.id", onupdate='CASCADE', ondelete='CASCADE')),
    Column("lang_model_id", Integer, ForeignKey("lang_model_files.id", onupdate='CASCADE', ondelete='CASCADE'))
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    meta.create_all()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    meta.drop_all()
