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
import fnmatch
import hashlib

#サードパーティパッケージ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
import sanakin
import sanakin.db as db
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

Session = sessionmaker(bind=ENGINE)

db.init(ENGINE)

def insert_corpus(cname, csymbol):
    c = db.Corpus(
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

def insert_snkfile(file_path, corpus_id):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * h.block_size), b''):
            h.update(chunk)
    checksum = h.hexdigest()

    target_file = db.SNKFile(
        name=os.path.basename(file_path),
        checksum=checksum,
        corpus_id=corpus_id
    )

    LOGGER.info(f'name:\t\t{target_file.name}')
    LOGGER.info(f'checksum:\t{target_file.checksum}')
    LOGGER.info('')

    session = Session()
    query = session.query(db.SNKFile).filter(db.SNKFile.name == target_file.name)
    exists = session.query(query.exists()).scalar()
    if not exists:
        n = target_file.name
        session.add(target_file)
        session.commit()
        session.close()

        LOGGER.info(f'{n}:\t格納完了!')
        LOGGER.info('')
    else:
        in_file = query.one()
        if not in_file.checksum == target_file.checksum:
            session.close()
            raise sanakin.SNKException(
                f'DB:\t{in_file.name}\t{in_file.checksum}\n'+
                f'target:\t{target_file.name}\t{target_file.checksum}\n'+
                '一致しません!!!\n')
        else:
            LOGGER.info(f'{target_file.name}:\t格納済み!')
            LOGGER.info('')
            session.close()

if __name__ == '__main__':
    # 楽天データに特化した処理を記載
    insert_corpus(
        '楽天データセット::楽天トラベル::ユーザレビュー',
        'RTUR',)

    session = Session()
    c = session.query(db.Corpus).one()

    for file_name in sorted(os.listdir(RAKUTEN_TRAVEL_DIR)):
        if fnmatch.fnmatch(file_name, 'travel02_userReview[0-9]*'):
            file_path = os.path.join(RAKUTEN_TRAVEL_DIR, file_name)
            insert_snkfile(file_path, c.id)
