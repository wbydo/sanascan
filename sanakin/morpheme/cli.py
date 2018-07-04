from logging import getLogger
from itertools import chain

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.orm import aliased
import sqlalchemy.dialects.mysql as mysql

from .. import MorphologicalAnalysis
from .. import Morpheme
from ..cli_util.base_function import _bulk_insert
from ..const import MAX_SELECT_RECORD

LOGGER = getLogger(__name__)

def insert(session, *, is_develop_mode=True):
    def _insert(morphs):
        insert_stmt = mysql.insert(Morpheme)
        insert_stmt = insert_stmt.on_duplicate_key_update(
            id=insert_stmt.inserted.id
        )

        session.execute(insert_stmt, morphs)
        LOGGER.info(f'{len(morphs)}件挿入!!!')

    latest_morph_id = session.query(
        Morpheme.morpheme_id
    ).order_by(
        Morpheme.morpheme_id.desc()
    ).first()

    lmi = latest_morph_id
    idx = 1 if not lmi else int(lmi[0].replace('MO', '')) + 1

    while True:
        query = _query(session, max_req=MAX_SELECT_RECORD)

        columns = [i['name'] for i in query.column_descriptions]
        columns.remove('morpheme_id')

        morphs = []
        record = None
        for record in query:
            r = dict([
                ('morpheme_id', f'MO{idx:0>8}'),
                *zip(columns,record)
            ])

            LOGGER.info(
                '{}:\t{}'.format(
                    r['morpheme_id'],
                    ','.join([r[c] if r[c] else '*'  for c in columns])
                )
            )

            morphs.append(r)
            idx += 1

        if record is None:
            break
        _insert(morphs) #ON_DUPLICATEにしたい

def delete(session):
    session.query(Morpheme).delete()

def _query(session, *, max_req=100):
    columns = MorphologicalAnalysis.__table__.columns.keys()
    for r in ['id', 'sentence_id', 'morphological_analysies_id', 'nth', 'length']:
        columns.remove(r)

    ma_c = lambda : (getattr(MorphologicalAnalysis, c) for c in columns)
    uma_sq = session.query(
        *ma_c()
    ).group_by(
        *ma_c()
    ).subquery('uma')
    uma = aliased(MorphologicalAnalysis, uma_sq)

    m_c = lambda : (getattr(Morpheme, c) for c in columns)
    m_sq = session.query(
        Morpheme.morpheme_id,
        *m_c()
    ).subquery('m')
    m = aliased(Morpheme, m_sq)

    uma_c = lambda : (getattr(uma, c) for c in columns)
    con = lambda : (
        or_(
            getattr(uma, c) == getattr(m, c),
            and_(
                getattr(uma, c) == None,
                getattr(m, c) == None
            )
        ) for c in columns
    )

    sq = session.query(
        *chain(
            uma_c(),
            [m.morpheme_id]
        )
    ).outerjoin(
        m, and_(*con())
    ).subquery('candidate')
    candidate = aliased(sq)

    q = session.query(
        candidate
    ).filter(
        candidate.c.morpheme_id == None
    ).limit(MAX_SELECT_RECORD)

    return q
