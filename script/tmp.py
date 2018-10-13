#組み込みパッケージ
import os
import sys
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
from sanakin import SNKSession
from sanakin.snkmecab import SNKMeCab
from sanakin import Sentence

from sanakin.cli_util import SNKCLIEngine
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
        pass

    def _sandbox_mode(self):
        pass

    def _non_wrapped_insert_mode(self, *, is_develop_mode=True):
        from sanakin.cleaner import Cleaner
        with SNKMeCab() as mecab:
            with SNKSession() as s:
                q = s.query(Sentence).limit(300)
                iter_ = map(lambda s1: s1.text, q)
                c = Cleaner()
                for s2 in c.clean(iter_, mecab):
                    print([str(i) for i in s2])

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = SeedEngine()
    cli.run()
