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
from sanakin import Corpus

import sanakin.corpus.cli as corpus
import sanakin.corpus_file.cli as corpus_file
import sanakin.corpus_data.cli as corpus_data
import sanakin.sentence_delimiter.cli as delimiter
import sanakin.sentence.cli as sentence

from sanakin.cli_util import SNKCLIEngine

from env import RAKUTEN_TRAVEL_DIR

# ロガー設定
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

def delete_mode(session):
    corpus.delete(session, 'CPRTUR')
    delimiter.delete(session, 'SD0001')

    for t in session.get_bind().table_names():
        q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
        session.execute(q.format(t))

def sandbox_mode(session):
    pass

def insert_mode(session, *, is_develop_mode=True):
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

    c = session.query(Corpus).one()

    for idx, file_name in enumerate(sorted(os.listdir(RAKUTEN_TRAVEL_DIR))):
        if is_develop_mode and idx == 1:
            break

        if fnmatch.fnmatch(file_name, 'travel02_userReview[0-9]*'):
            file_path = os.path.join(RAKUTEN_TRAVEL_DIR, file_name)
            corpus_file.insert(session, file_path, c.corpus_id)

    corpus_data.insert(
        session,
        c.corpus_id,
        RAKUTEN_TRAVEL_DIR,
        is_develop_mode
    )

    sentence.insert(
        session,
        'SD0001',
        is_develop_mode
    )

if __name__ == '__main__':
    cli = SNKCLIEngine(
            description='''\
                DBに初期データを投入するためのCLI。
                引数なしで実行した場合、開発モードとしてRTURのサブセットをinsert。\
            ''',
            del_msg='RTURのすべてのseedデータ'
    )

    cli.delete_mode = delete_mode
    cli.sandbox_mode = sandbox_mode
    cli.insert_mode = insert_mode
    cli.run()
