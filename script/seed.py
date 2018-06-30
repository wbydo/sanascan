#組み込みパッケージ
import os
import sys
from contextlib import contextmanager
import argparse
import fnmatch

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
import sanakin.corpus.cli as corpus
import sanakin.corpus_file.cli as corpus_file
import sanakin.corpus_data.cli as corpus_data

from env import TARGET_DB, RAKUTEN_TRAVEL_DIR

DATABASE = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
      TARGET_DB['user_name'],
      TARGET_DB['password'],
      TARGET_DB['host_ip'],
      TARGET_DB['db_name']
)

ENGINE = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=False
)

@contextmanager
def Session(engine):
    sanakin.init(engine)

    _Session = sessionmaker(bind=engine)
    session = _Session()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# ロガー設定
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='''\
                DBに初期データを投入するためのCLI。
                引数なしで実行した場合、開発モードとしてRTURのサブセットをinsert。\
            ''',
            formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-d', '--delete',
        action='store_true',
        help='RTURのすべてのデータを削除'
    )

    group.add_argument(
        '-a', '--all',
        action='store_true',
        help='RTURのすべてのデータをinsert'
    )
    args = parser.parse_args()

    if args.delete:
        while True:
            ans = input('RTURのすべてのデータを削除しますか？[Y/n] ')
            if ans in ['Y', 'n']:
                break

        if ans == 'Y':
            with Session(ENGINE) as session:
                corpus.delete(session, 'RTUR')

    # deleteモードでないとき
    else:
        develop_mode = not args.all

        with Session(ENGINE) as session:
            corpus.insert(
                session,
                '楽天データセット::楽天トラベル::ユーザレビュー',
                'RTUR'
            )

            c = session.query(sanakin.Corpus).one()

            for idx, file_name in enumerate(sorted(os.listdir(RAKUTEN_TRAVEL_DIR))):
                if develop_mode and idx == 1:
                    break

                if fnmatch.fnmatch(file_name, 'travel02_userReview[0-9]*'):
                    file_path = os.path.join(RAKUTEN_TRAVEL_DIR, file_name)
                    corpus_file.insert(session, file_path, c.corpus_id)

            corpus_data.insert(
                session,
                ENGINE,
                c.corpus_id,
                RAKUTEN_TRAVEL_DIR,
                develop_mode
            )
