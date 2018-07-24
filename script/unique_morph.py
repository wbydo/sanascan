#組み込みパッケージ
import os
import sys
import pathlib

from sqlalchemy.orm import aliased
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import distinct
from sqlalchemy import func

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
from sanakin import Sentence
from sanakin import TmpMorpheme
from sanakin import SplitedSentence
from sanakin import Morpheme

from sanakin import SNKMeCab
from sanakin import SNKSession
from sanakin.cli_util import SNKCLIEngine
from sanakin.cli_util.db_api import limit_select
from sanakin.cli_util.db_api import bulk_insert

from sanakin.const import MAX_SELECT_RECORD

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

    @SNKCLIEngine.confirm(msg=f'{_work}:消去しますか？')
    def _delete_mode(self):
        with SNKSession() as session:
            with session.commit_manager() as s:
                s.query(Morpheme).delete()

                q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
                for t in session.get_bind().table_names():
                    session.execute(q.format(t))

    def _sandbox_mode(self):
        pass

    def _query(self):
        def _cond(klass1, klass2, f):
            return or_(
                getattr(klass1, f) == getattr(klass2, f),
                and_(
                    getattr(klass1, f) == None,
                    getattr(klass2, f) == None
                )
            )

        # tmp_morphemesにmorphemesを外部結合して
        # morpheme_idがnullのものを抽出して
        # 重複を除くクエリ
        with SNKSession() as s:
            query = s.query(
                *[getattr(TmpMorpheme, f) for f in ['surface', *TmpMorpheme.FEATURES]],
            ).outerjoin(
                Morpheme,
                and_(
                    *[_cond(TmpMorpheme, Morpheme, f) for f in ['surface', *TmpMorpheme.FEATURES]]
                ),
                aliased=True, from_joinpoint=True
            ).filter(
                Morpheme.morpheme_id == None
            ).group_by(
                *[getattr(TmpMorpheme, f) for f in ['surface', *TmpMorpheme.FEATURES]]
            ).limit(MAX_SELECT_RECORD)

        return query

    def _non_wrapped_insert_mode(self, *, is_develop_mode=True):
        with SNKSession() as s:
            last_morpheme_id = s.query(Morpheme.morpheme_id).order_by(
                Morpheme.morpheme_id.desc()
            ).limit(1).scalar()

        if last_morpheme_id is None:
            last_morpheme_id = 1
        else:
            last_morpheme_id = int(last_morpheme_id.replace('MO', '')) + 1

        while True:
            morphemes = []
            with SNKSession() as session:
                query = self._query().with_session(session)

                result = None
                for result in query:
                    m = Morpheme(**{f:result._asdict()[f] for f in ['surface', *TmpMorpheme.FEATURES]})
                    m.morpheme_id = 'MO{:0>10}'.format(last_morpheme_id)
                    morphemes.append(m)
                    last_morpheme_id += 1

                if result is None:
                    break

                with session.commit_manager() as s:
                    s.add_all(morphemes)


    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = UniqueMorphemeEngine()
    cli.run()
