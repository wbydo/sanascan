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
from sqlalchemy.dialects.mysql import insert

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

def insert_corpus(cname, corpus_id):
    c = db.Corpus(
        name=cname,
        corpus_id=corpus_id,)

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

def insert_corpus_file(file_path, corpus_id):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * h.block_size), b''):
            h.update(chunk)
    checksum = h.hexdigest()

    target_file = db.CorpusFile(
        corpus_file_id=os.path.basename(file_path),
        checksum=checksum,
        corpus_id=corpus_id
    )

    LOGGER.info(f'name:\t\t{target_file.corpus_file_id}')
    LOGGER.info(f'checksum:\t{target_file.checksum}')
    LOGGER.info('')

    session = Session()
    query = session.query(db.CorpusFile).filter(
        db.CorpusFile.corpus_file_id == target_file.corpus_file_id
    )
    exists = session.query(query.exists()).scalar()
    if not exists:
        n = target_file.corpus_file_id
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
                f'DB:\t{in_file.corpus_file_id}\t{in_file.checksum}\n'+
                f'target:\t{target_file.corpus_file_id}\t{target_file.checksum}\n'+
                '一致しません!!!\n')
        else:
            LOGGER.info(f'{target_file.corpus_file_id}:\t格納済み!')
            LOGGER.info('')
            session.close()

def insert_corpus_datum(corpus_id, file_dir):
    def process_all_line():
        session = Session()
        corpus = session.query(db.Corpus).filter(
            db.Corpus.corpus_id == corpus_id).one()
        corpus_files = corpus.corpus_files
        session.close()

        for corpus_file in corpus_files:
            for line in corpus_file.readline(RAKUTEN_TRAVEL_DIR):
                extracted = corpus.extract_data(line)
                result =  {
                    'corpus_data_id': ''.join([
                        corpus.corpus_id,
                        '{:0>8}'.format(extracted['id_in_corpus'])
                    ]),
                    'corpus_file_id':corpus_file.corpus_file_id,
                    'id_in_corpus': extracted['id_in_corpus'],
                    'text': extracted['text'],
                }
                LOGGER.info('proccess_file: ' + str(result['corpus_data_id']) + '  ' + result['text'][:20])
                yield result

    def insert_(corpus_datam):
        insert_stmt = insert(db.CorpusData)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            corpus_file_id=insert_stmt.inserted.corpus_file_id,
            id_in_corpus=insert_stmt.inserted.id_in_corpus,
            text=insert_stmt.inserted.text,
            corpus_data_id=insert_stmt.inserted.corpus_data_id,
        )
        with ENGINE.begin() as conn:
            conn.execute(on_duplicate_key_stmt, datum)

    datum = []
    max_size = 500_000_000
    for d in process_all_line():
        if sys.getsizeof(datum) < max_size:
            datum.append(d)
        else:
            LOGGER.info(f'INSERT: {len(datum)}件挿入!!!')
            insert_(datum)
            datum = []
    if datum:
        LOGGER.info(f'INSERT: {len(datum)}件挿入!!!')
        insert_(datum)

if __name__ == '__main__':
    # 楽天データに特化した処理を記載
    insert_corpus(
        '楽天データセット::楽天トラベル::ユーザレビュー',
        'RTUR',)

    session = Session()
    c = session.query(db.Corpus).one()
    session.close()

    # for file_name in sorted(os.listdir(RAKUTEN_TRAVEL_DIR)):
    #     if fnmatch.fnmatch(file_name, 'travel02_userReview[0-9]*'):
    #         file_path = os.path.join(RAKUTEN_TRAVEL_DIR, file_name)
    #         insert_corpus_file(file_path, c.corpus_id)

    insert_corpus_datum(c.corpus_id, RAKUTEN_TRAVEL_DIR)
