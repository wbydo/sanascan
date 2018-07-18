#組み込みパッケージ
import os
import sys
import pathlib

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
from sanakin import CorpusData
from sanakin import SentenceDelimiter
from sanakin import Sentence

from sanakin import SNKSession
from sanakin.cli_util import SNKCLIEngine
from sanakin.cli_util.db_api import limit_select
from sanakin.cli_util.db_api import bulk_insert

from env import RAKUTEN_TRAVEL_DIR

# ロガー設定
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

class SentenceEngine(SNKCLIEngine):
    _work = 'sentence'

    def __init__(self):
        super(__class__, self).__init__(
            description='''\
                データから分を抽出するためのCLI。\
            '''
        )

    @SNKCLIEngine.confirm(msg=f'{_work}:消去しますか？')
    def _delete_mode(self):
        with SNKSession() as session:
            with session.commit_manager() as s:
                s.query(Sentence).delete()

                q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
                for t in session.get_bind().table_names():
                    session.execute(q.format(t))

    def _sandbox_mode(self):
        pass

    def _non_wrapped_insert_mode(self, *, is_develop_mode=True):
        with SNKSession() as s:
            sd = s.query(SentenceDelimiter).one()
            q = s.query(CorpusData)

        def iter_():
            for d in limit_select(q, CorpusData.id):
                for s in Sentence.create_iter(d, sd):
                    yield s

        bulk_insert(iter_(), Sentence, is_develop_mode=is_develop_mode)

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = SentenceEngine()
    cli.run()
