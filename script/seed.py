# ロガー設定
from logging import getLogger,StreamHandler,DEBUG
LOGGER = getLogger(__name__)
LOGGER.setLevel(DEBUG)

HANDLER = StreamHandler()
HANDLER.setLevel(DEBUG)
LOGGER.addHandler(HANDLER)

#組み込みパッケージ
import os
import sys

#サードパーティパッケージ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
import sanakin.db
from env import TARGET_DB

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

Session = sessionmaker(bind=ENGINE)

sanakin.db.init(ENGINE)

def insert_corpus(cname, csymbol):
    c = sanakin.db.Corpus(
        name=cname,
        symbol=csymbol,)

    session = Session()

    try:
        session.add(c)
        session.commit()
    except Exception as e:
        err_code, _ = e.orig.args
        if err_code == 1062:
            LOGGER.info('格納済み')
        else:
            raise e
    finally:
        session.close()

if __name__ == '__main__':
    insert_corpus(
        '楽天データセット::楽天トラベル::ユーザレビュー',
        'RTUR',)
