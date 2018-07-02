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

def limit_select(query, class_id, *, max_req=1000):
    # 参考: https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/WindowedRangeQuery

    first_id = None
    while True:
        q = query
        if first_id is not None:
            q = query.filter(class_id > first_id)

        record = None
        for record in q.order_by(class_id).limit(max_req):
            yield record

        if record is None:
            break
        first_id = class_id.__get__(record, class_id) if record else None
