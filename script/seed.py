#組み込みパッケージ
import os
import sys
from contextlib import contextmanager
import argparse

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

@contextmanager
def Session():
    database = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
          TARGET_DB['user_name'],
          TARGET_DB['password'],
          TARGET_DB['host_ip'],
          TARGET_DB['db_name']
    )

    engine = create_engine(
        database,
        encoding='utf-8',
        echo=True
    )

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='''\
                DBに初期データを投入するためのCLI。
                引数なしで実行した場合、開発モードとしてRTURのサブセットをinsert。\
            ''',
            formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-d', '--delete',
        action='store_true',
        help='RTURのすべてのデータを削除'
    )
    args = parser.parse_args()

    if args.delete:
        while True:
            ans = input('RTURのすべてのデータを削除しますか？[Y/n] ')
            if ans in ['Y', 'n']:
                break

        if ans == 'Y':
            with Session() as session:
                corpus.delete(session, 'RTUR')

    else:
        pass
