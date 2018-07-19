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

class MorphemeEngine(SNKCLIEngine):
    _work = 'morpheme'

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
                s.query(TmpMorpheme).delete()

                q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
                for t in session.get_bind().table_names():
                    session.execute(q.format(t))

    def _sandbox_mode(self):
        pass

    def _sentence_query_untill_not_splited(self):
        with SNKSession() as s:
            inserted_tmp_morpheme_subq = s.query(TmpMorpheme.sentence_id).filter(
                TmpMorpheme.nth == TmpMorpheme.length,
            ).subquery('itm')

            itm = aliased(TmpMorpheme, inserted_tmp_morpheme_subq)

            q = s.query(Sentence).outerjoin(
                inserted_tmp_morpheme_subq,
                Sentence.sentence_id == itm.sentence_id
            ).filter(itm.sentence_id == None)

        return q

    def _non_wrapped_insert_mode(self, *, is_develop_mode=True):
        q = self._sentence_query_untill_not_splited()

        def iter_():
            with SNKMeCab() as mecab:
                for sen in limit_select(q, Sentence.id):
                    for m in TmpMorpheme.create_iter(sen, mecab):
                        yield m

        bulk_insert(iter_(), TmpMorpheme, is_develop_mode=is_develop_mode)

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = MorphemeEngine()
    cli.run()
