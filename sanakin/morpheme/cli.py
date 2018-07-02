from logging import getLogger
from itertools import chain

from sqlalchemy import and_
from sqlalchemy.orm import aliased

from .. import MorphologicalAnalysis
from .. import Morpheme
from ..cli_util.db_api import limit_select
from ..cli_util.base_function import _bulk_insert

LOGGER = getLogger(__name__)

def insert(session, *, is_develop_mode=True):
    def _iterator():
        res = session.query(
            Morpheme.morpheme_id
        ).order_by(
            Morpheme.morpheme_id.desc()
        ).first()

        idx = 1 if not res else int(res[0].replace('MO', ''))

        while True:
            query = _query(session, max_req=2)

            columns = [i['name'] for i in query.column_descriptions]
            columns.remove('morpheme_id')

            for record in query:
                yield dict([
                    ('morpheme_id', f'MO{idx+1:0>8}'),
                    *zip(columns,record)
                ])
                idx += 1

            if record is None:
                break

    _bulk_insert(
        session,
        _iterator(),
        Morpheme,
        LOGGER,
        is_develop_mode=is_develop_mode
    )

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
    con = lambda : (getattr(uma, c) == getattr(m, c) for c in columns)
    query = session.query(
        *chain(
            uma_c(),
            [m.morpheme_id]
        )
    ).outerjoin(
        m, and_(
            *con()
        )
    ).filter(m.morpheme_id == None).limit(max_req)

    return query
