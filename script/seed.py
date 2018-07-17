#組み込みパッケージ
import os
import sys
from contextlib import contextmanager
import argparse
import fnmatch
import pathlib

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
from sanakin import Corpus
from sanakin import SentenceDelimiter
from sanakin import CorpusFile

from sanakin.cli_util import SNKCLIEngine
from sanakin.cli_util import SNKSession
from sanakin.cli_util.db_api import simple_insert
from sanakin.cli_util.db_api import bulk_insert

from env import RAKUTEN_TRAVEL_DIR

# ロガー設定
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

class SeedEngine(SNKCLIEngine):
    _work = 'seed'

    def __init__(self):
        super(__class__, self).__init__(
            description='''\
                DBに初期データを投入するためのCLI。
                引数なしで実行した場合、開発モードとしてRTURのサブセットをinsert。\
            '''
        )

    @SNKCLIEngine.confirm(msg=f'{_work}:消去しますか？')
    def _delete_mode(self):
        with SNKSession() as session:
            with session.commit_manager() as s:
                s.query(Corpus).filter(
                    Corpus.corpus_id == 'CPRTUR'
                ).delete()

                s.query(SentenceDelimiter).filter(
                    SentenceDelimiter.sentence_delimiter_id == 'SD0001'
                ).delete()

                q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
                for t in session.get_bind().table_names():
                    session.execute(q.format(t))

    def _sandbox_mode(self):
        pass

    def _non_wrapped_insert_mode(self, *, is_develop_mode=True):
        corpus = Corpus(
            corpus_id='CPRTUR',
            name='楽天データセット::楽天トラベル::ユーザレビュー',
        )
        simple_insert(corpus)

        delimiter = SentenceDelimiter(
            sentence_delimiter_id='SD0001',
            regex=r'[。．\.！!？\?\n]+',
        )
        simple_insert(delimiter)

        dir_ = pathlib.Path(RAKUTEN_TRAVEL_DIR)

        corpus_files = []
        with SNKSession() as session:
            session.add(corpus)
            for idx, file_path in enumerate(dir_.iterdir()):
                if is_develop_mode and idx == 1:
                    break

                if fnmatch.fnmatch(file_path.name, 'travel02_userReview[0-9]*'):
                    cf = CorpusFile.create(file_path)
                    cf.corpus_id = corpus.corpus_id
                    corpus_files.append(cf)

        bulk_insert(corpus_files, CorpusFile)

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = SeedEngine()
    cli.run()
