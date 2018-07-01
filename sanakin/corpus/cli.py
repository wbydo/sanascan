from logging import getLogger

from ..base_cli import _simple_insert
from ..base_cli import _simple_delete

from .. import Corpus

LOGGER = getLogger(__name__)

def insert(session, cname, corpus_id):
    func = _simple_insert(
        Corpus,
        LOGGER,
        'name',
        'corpus_id'
    )
    func(session, cname, corpus_id)

def delete(session, corpus_id):
    func = _simple_delete(Corpus, 'corpus_id')
    func(session, corpus_id)
