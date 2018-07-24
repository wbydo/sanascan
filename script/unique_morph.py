#組み込みパッケージ
import os
import sys
import pathlib

from sqlalchemy.orm import aliased
from sqlalchemy import and_

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
from sanakin import Sentence
from sanakin import TmpMorpheme

from sanakin import SNKMeCab
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

class UniqueMorphemeEngine(SNKCLIEngine):
    _work = 'unique_morpheme'

    def __init__(self):
        super(__class__, self).__init__(
            description='''\
                ユニークな形態素を抽出するためのCLI。\
            '''
        )

    @SNKCLIEngine.confirm(msg=f'{_work}:消去しますか？[前段の処理にも影響するから注意]')
    def _delete_mode(self):
        pass

    def _sandbox_mode(self):
        pass

    def _non_wrapped_insert_mode(self, *, is_develop_mode=True):
        pass

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = UniqueMorphemeEngine()
    cli.run()
