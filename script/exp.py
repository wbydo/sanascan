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
        # from sanakin import MorphologicalAnalysis
        # from sanakin import Morpheme
        # from sqlalchemy.orm import aliased
        # from sqlalchemy import and_
        # from itertools import chain
        # from sanakin.cli_util.db_api import limit_select
        #
        # columns = MorphologicalAnalysis.__table__.columns.keys()
        # for r in ['id', 'sentence_id', 'morphological_analysies_id', 'nth', 'length']:
        #     columns.remove(r)
        #
        # ma_c = lambda : (getattr(MorphologicalAnalysis, c) for c in columns)
        # uma_sq = session.query(
        #     *ma_c()
        # ).group_by(
        #     *ma_c()
        # ).subquery('uma')
        # uma = aliased(MorphologicalAnalysis, uma_sq)
        #
        # m_c = lambda : (getattr(Morpheme, c) for c in columns)
        # m_sq = session.query(
        #     Morpheme.morpheme_id,
        #     *m_c()
        # ).subquery('m')
        # m = aliased(Morpheme, m_sq)
        #
        # uma_c = lambda : (getattr(uma, c) for c in columns)
        # con = lambda : (getattr(uma, c) == getattr(m, c) for c in columns)
        # q = session.query(
        #     *chain(
        #         uma_c(),
        #         [m.morpheme_id]
        #     )
        # ).outerjoin(
        #     m, and_(
        #         *con()
        #     )
        # ).filter(m.morpheme_id == None).limit(2)
        #
        # columns_ = [i['name'] for i in q.column_descriptions]
        # columns_.remove('morpheme_id')
        #
        # for i in q:
        #     print(len(dict(zip(columns_, i))))
        from sanakin.morpheme.cli import insert
        insert(session, is_develop_mode=True)

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
