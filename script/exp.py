import os
import sys

from natto import MeCab

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

import sanakin.morphological_analysis.cli as manalysis
from sanakin.cli_util import SNKCLIEngine

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
        manalysis.delete(session)
        q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
        for t in ['morphological_analysies']:
            session.execute(q.format(t))

    def _sandbox_mode(self, session):
        import sanakin
        cf = session.query(sanakin.CorpusFile).first()
        print(cf)
        print(cf.origin_datum)

    def _non_wrapped_insert_mode(self, session, *, is_develop_mode=True):
        with MeCab() as mecab:
            manalysis.insert(
                session,
                mecab,
                is_develop_mode=is_develop_mode
            )

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, session, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(session, is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = ExpEngine()
    cli.run()
