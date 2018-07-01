from logging import getLogger

from ..cli_util.base_function import _simple_insert
from ..cli_util.base_function import _simple_delete

from ..mapped_classes import SentenceDelimiter

LOGGER = getLogger(__name__)

def insert(session, regex, sentence_delimiter_id):
    func = _simple_insert(
        SentenceDelimiter,
        LOGGER,
        'regex',
        'sentence_delimiter_id'
    )
    func(session, regex, sentence_delimiter_id)

def delete(session, sentence_delimiter_id):
    func = _simple_delete(
        SentenceDelimiter,
        'sentence_delimiter_id'
    )
    func(session,sentence_delimiter_id)
