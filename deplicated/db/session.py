from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def database(user_name, password, host_ip, db_name):
    # 書式 → dialect+driver://username:password@host:port/database
    # ソース : https://qiita.com/t2kojima/items/5c7f9978f98b1a897d73

    return 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
        user_name,
        password,
        host_ip,
        db_name
    )

def engine_and_session(database, echo=True):
    ENGINE = create_engine(
        database,
        encoding='utf-8',
        echo=echo
    )

    Session = sessionmaker(bind=ENGINE)
    return ENGINE, Session
