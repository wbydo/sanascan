import sqlalchemy

from .mapped_classes import Base
from .snksession import SNKSession


def init(*, username, password, host, database):
    db = f'mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8' # noqa

    engine = sqlalchemy.create_engine(
        db,
        encoding='utf-8',
        echo=False,
        pool_size=20,
        max_overflow=10
    )

    Base.prepare(engine, reflect=True)
    SNKSession.configure(bind=engine)
