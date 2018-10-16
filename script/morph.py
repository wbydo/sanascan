#組み込みパッケージ
import os
import sys
import pathlib
from itertools import chain

from sqlalchemy.orm import aliased
from sqlalchemy import and_
from sqlalchemy import or_

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

# logging.basicConfig()
# root_logger = logging.getLogger()
# streamHandler = root_logger.handlers[0]
# root_logger.removeHandler(streamHandler)
#
# loggers = [
#     __name__ + '.copy',
#     'sqlalchemy.engine',
#     'sanakin.cli_util.db_api',
#     __name__ + '.insert_mode',
# ]

# for l in loggers:
#     logger = logging.getLogger(l)
#     logger.addHandler(streamHandler)
#     logger.setLevel(logging.DEBUG)

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
                s.query(Morpheme).delete()
                s.query(TmpMorpheme).delete()
                s.query(SplitedSentence).delete()

                q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
                for t in session.get_bind().table_names():
                    session.execute(q.format(t))

    @staticmethod
    def _sentence_query_untill_not_splited():
        with SNKSession() as s:
            sq = s.query(SplitedSentence).filter(
                SplitedSentence.nth == SplitedSentence.length
            ).subquery('sps')

            sps = aliased(SplitedSentence, sq)

            q = s.query(Sentence).outerjoin(
                sps,
                Sentence.sentence_id == sps.sentence_id
            ).filter(
                sps.id == None
            ).limit(MAX_SELECT_RECORD)

        return q

    @staticmethod
    def _null_or_equal_condition(klass1, klass2, feature):
        return or_(
            getattr(klass1, feature) == getattr(klass2, feature),
            and_(
                getattr(klass1, feature) == None,
                getattr(klass2, feature) == None
            )
        )

    @classmethod
    def _query_of_unique_morpheme(klass):
        nu = lambda c1, c2, f: klass._null_or_equal_condition(c1, c2, f)

        with SNKSession() as s:
            query = s.query(
                *[getattr(TmpMorpheme, f) for f in ['surface', *TmpMorpheme.FEATURES]],
            ).outerjoin(
                Morpheme,
                and_(
                    *[nu(TmpMorpheme, Morpheme, f) for f in ['surface', *TmpMorpheme.FEATURES]]
                ),
            ).filter(
                Morpheme.morpheme_id == None
            ).group_by(
                *[getattr(TmpMorpheme, f) for f in ['surface', *TmpMorpheme.FEATURES]]
            )

        return query

    @classmethod
    def _query_of_splited_sentence(klass):
        nu = lambda c1, c2, f: klass._null_or_equal_condition(c1, c2, f)

        with SNKSession() as s:
            query = s.query(
                TmpMorpheme.sentence_id,
                TmpMorpheme.nth,
                TmpMorpheme.length,
                Morpheme.morpheme_id
            ).join(
                Morpheme,
                and_(
                    *[nu(TmpMorpheme, Morpheme, f) for f in ['surface', *TmpMorpheme.FEATURES]]
                ),
            )

        return query

    @classmethod
    def _insert_splited_sentence(klass):
        with SNKSession() as session:
            query = klass._query_of_splited_sentence().with_session(session)

            f = lambda r: SplitedSentence(**r._asdict())

            ss = []
            for i in query:
                s = f(i)
                ss.append(s)

        bulk_insert(ss, SplitedSentence)

    @classmethod
    def _copy_to_morphemes_table_from_tmp(klass):
        logger = logging.getLogger(__name__ + '.copy')
        logger.debug('first-of-function')

        with SNKSession() as s:
            last_morpheme_id = s.query(Morpheme.morpheme_id).order_by(
                Morpheme.morpheme_id.desc()
            ).limit(1).scalar()

        if last_morpheme_id is None:
            last_morpheme_id = 1
        else:
            last_morpheme_id = int(last_morpheme_id.replace('MO', '')) + 1

        logger.debug(f'last_morpheme_id: {last_morpheme_id}')

        with SNKSession() as session:
            query = klass._query_of_unique_morpheme().with_session(session)

        morphemes = []
        for result in query:
            m = Morpheme(**{f:result._asdict()[f] for f in ['surface', *TmpMorpheme.FEATURES]})
            m.morpheme_id = 'MO{:0>10}'.format(last_morpheme_id)
            morphemes.append(m)
            last_morpheme_id += 1

        logger.debug('bulk_insert')
        bulk_insert(iter(morphemes), Morpheme)

    def _sandbox_mode(self):
        with SNKSession() as session:
            with session.commit_manager() as s:
                s.query(Morpheme).delete()
                s.query(TmpMorpheme).delete()
                s.query(SplitedSentence).delete()

                q = 'ALTER TABLE {} AUTO_INCREMENT = 1;'
                for t in session.get_bind().table_names():
                    session.execute(q.format(t))

    def _non_wrapped_insert_mode(self, *, is_develop_mode=True):
        if is_develop_mode:
            print('develop_mode未実装')
            print(' -a で一気に入れるしかない')

        else:
            with SNKMeCab() as mecab:
                while True:
                    q = self._sentence_query_untill_not_splited()
                    with SNKSession() as s:
                        query = q.with_session(s)

                    sentence = None

                    sentences = []
                    for sentence in query:
                        sentences.append(sentence)

                    if sentence is None:
                        break

                    else:
                        logger_blA = logging.getLogger(__name__ + '.insert_mode')

                        f = lambda s: TmpMorpheme.create_iter(s, mecab)
                        bulk_insert(chain(*map(f, sentences)), TmpMorpheme)
                        logger_blA.debug('log-1')

                        self.__class__._copy_to_morphemes_table_from_tmp()
                        logger_blA.debug('log-2')

                        self.__class__._insert_splited_sentence()
                        logger_blA.debug('log-3')

                        with SNKSession() as s:
                            with s.commit_manager() as sc:
                                sc.query(TmpMorpheme).delete()

    @SNKCLIEngine.confirm(msg=f'{_work}:時間がかかりますがいいですか？')
    def _long_time_insert_mode(self, *, is_develop_mode=True):
        self._non_wrapped_insert_mode(is_develop_mode=is_develop_mode)

if __name__ == '__main__':
    cli = MorphemeEngine()
    cli.run()
