import os
import sys

from natto import MeCab

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

from sanakin import Sentence, Morpheme, MorphemeDict
from sanakin.cli_util import SNKCLIEngine
from sanakin.cli_util import SNKSession
from sanakin.cli_util.db_api import limit_select
from sanakin.cli_util.db_api import bulk_insert

# ロガー設定
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

class ExpEngine(SNKCLIEngine):
    _work = 'experiment'

    def __init__(self):
        super(__class__, self).__init__(
            description='''\

                !!! 形態素解析用のスクリプトだぞ !!!

                DBに形態素解析結果を投入するためのCLI。
                引数なしで実行した場合、100件だけやる。\
            '''
        )

    @SNKCLIEngine.confirm(msg=f'{_work}:消去しますか？')
    def _delete_mode(self, session):
        q = f'TRUNCATE TABLE {Morpheme.__tablename__};'

        with SNKSession() as s:
            s.execute(q)

    def _sandbox_mode(self):
        pass

    def _non_wrapped_insert_mode(self, session, *, is_develop_mode=True):
        def _iterator(query, mecab):
            for sentence in limit_select(query, Sentence.id):
                for morph in Morpheme.create(sentence, mecab):
                    yield morph

        with SNKSession() as session, MeCab() as mecab:
            q = session.query(Sentence)

            bulk_insert(
                _iterator(q, mecab),
                Morpheme,
                is_develop_mode=is_develop_mode
            )

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, session, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(session, is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = ExpEngine()
    cli.run()
