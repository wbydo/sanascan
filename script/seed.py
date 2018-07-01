#組み込みパッケージ
import os
import sys
from contextlib import contextmanager
import argparse
import fnmatch

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
import sanakin.sentence_delimiter.cli as delimiter
import sanakin.sentence.cli as sentence

from sanakin.cli_util.db_api import sessionmaker_

from env import RAKUTEN_TRAVEL_DIR

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

    parser.add_argument('CONFIG', help='config.yml')
    parser.add_argument(
        '-E', '--environment',
        default='develop',
        help='DB環境の指定'
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

    group.add_argument(
        '--dev',
        action='store_true',
        help='実験用'
    )

    args = parser.parse_args()

    Session = sessionmaker_(args.CONFIG, args.environment)

    # DELETEモード
    if args.delete:
        while True:
            ans = input('RTURのすべてのデータを削除しますか？[Y/n] ')
            if ans in ['Y', 'n']:
                break

        if ans == 'Y':
            with Session() as session:
                corpus.delete(session, 'CPRTUR')
                delimiter.delete(session, 'SD0001')

                for t in session.get_bind().table_names():
                    q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
                    session.execute(q.format(t))

    # 実験用
    elif args.dev:
        pass
    # DELETEモードでないとき
    else:
        develop_mode = not args.all

        with Session() as session:
            corpus.insert(
                session,
                '楽天データセット::楽天トラベル::ユーザレビュー',
                'CPRTUR'
            )

            delimiter.insert(
                session,
                # r'(?P<period>(?:。|．|\.|！|!|？|\?)+)',
                r'[。．\.！!？\?\n]+',
                'SD0001'
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
                c.corpus_id,
                RAKUTEN_TRAVEL_DIR,
                develop_mode
            )

            sentence.insert(
                session,
                'SD0001',
                develop_mode
            )
