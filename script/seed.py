# ロガー設定
from logging import getLogger,StreamHandler,DEBUG
LOGGER = getLogger('sanakin.corpus_data.cli')
LOGGER.setLevel(DEBUG)

HANDLER = StreamHandler()
HANDLER.setLevel(DEBUG)
LOGGER.addHandler(HANDLER)

#組み込みパッケージ
import os
import sys
import fnmatch
import hashlib
from contextlib import contextmanager

#サードパーティパッケージ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
import sanakin
import sanakin.corpus.cli as corpus
import sanakin.corpus_file.cli as corpus_file
import sanakin.corpus_data.cli as corpus_data
from env import TARGET_DB, RAKUTEN_TRAVEL_DIR

# 定数
DATABASE = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
      TARGET_DB['user_name'],
      TARGET_DB['password'],
      TARGET_DB['host_ip'],
      TARGET_DB['db_name']
)

ENGINE = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=True
)

@contextmanager
def Session():
    _Session = sessionmaker(bind=ENGINE)
    session = _Session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

sanakin.init(ENGINE)

if __name__ == '__main__':
    with Session() as session:
        corpus.insert(
            session,
            '楽天データセット::楽天トラベル::ユーザレビュー',
            'RTUR',
        )

        c = session.query(sanakin.Corpus).one()

        # file_name = 'travel02_userReview00_20160304.txt'
        # file_path = os.path.join(RAKUTEN_TRAVEL_DIR, file_name)
        # corpus_file.insert(session, file_path, c.corpus_id)

        # 選べるようにする
        corpus_data.insert(session, ENGINE, c.corpus_id, RAKUTEN_TRAVEL_DIR)
