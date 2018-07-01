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

class SeedEngine(SNKCLIEngine):
    def __init__(self):
        super(__class__, self).__init__(
            description='''\
                DBに初期データを投入するためのCLI。
                引数なしで実行した場合、開発モードとしてRTURのサブセットをinsert。\
            '''
        )

    def _delete_mode(self, session):
        self.confirm(msg='seed: 消去しますか？')(
            self._non_wrapped_delete_mode
        )(session)

    def _non_wrapped_delete_mode(self, session):
        corpus.delete(session, 'CPRTUR')
        delimiter.delete(session, 'SD0001')

        for t in session.get_bind().table_names():
            q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
            session.execute(q.format(t))

    def _sandbox_mode(self, session):
        pass

    # expと同じ。DRYじゃない。
    # 気に入らないがガマン
    def _insert_mode(self, session, *, is_develop_mode=True):
        if is_develop_mode:
            self._non_wrapped_insert_mode(session, is_develop_mode=is_develop_mode)

        else:
            self.confirm(msg='seed: 時間がかかりますがいいですか？')(
                self._non_wrapped_insert_mode
            )(session, is_develop_mode=is_develop_mode)

    def _non_wrapped_insert_mode(self, session, *, is_develop_mode=True):
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
            is_develop_mode=is_develop_mode
        )

        sentence.insert(
            session,
            'SD0001',
            is_develop_mode=is_develop_mode
        )

if __name__ == '__main__':
    cli = SeedEngine()
    cli.run()
