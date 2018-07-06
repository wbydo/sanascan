import os
import sys

from natto import MeCab

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

from sanakin.cli_util import SNKCLIEngine
from sanakin import SNKSession

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
        from sanakin.err import SNKException
        raise SNKException('一時使用中止')

        morpheme.delete(session)
        morph_dict.delete(session)

    def _sandbox_mode(self):
        from sanakin import Sentence
        with SNKSession() as s:
            s = s.query(Sentence).first()
            print(s.text)

    def _non_wrapped_insert_mode(self, session, *, is_develop_mode=True):
        from sanakin.err import SNKException
        raise SNKException('一時使用中止')

        with MeCab() as mecab:
            morpheme.insert(
                session,
                mecab,
                is_develop_mode=is_develop_mode
            )
        morph_dict.insert(session, is_develop_mode=is_develop_mode)

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, session, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(session, is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = ExpEngine()
    cli.run()
