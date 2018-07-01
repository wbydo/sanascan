from contextlib import contextmanager

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..mapped_classes import Base
from ..err import SNKException

def sessionmaker_(file_path, environment):
    with open(file_path) as f:
        config = yaml.load(f)

    if not environment in config.keys():
        raise SNKException(f'環境名{environment}が見つからない')

    db = 'mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8'.format(
        **config[environment]
    )

    engine = create_engine(
        db,
        encoding='utf-8',
        echo=False
    )

    @contextmanager
    def Session():
        Base.prepare(engine, reflect=True)

        _Session = sessionmaker(bind=engine)
        session = _Session()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        else:
            session.commit()
        finally:
            session.close()

    return Session
