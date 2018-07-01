from logging import getLogger

import sqlalchemy.dialects.mysql as mysql

from .. import CorpusFile, CorpusData
from ..cli_util.base_function import _bulk_insert

LOGGER = getLogger(__name__)

def insert(session, corpus_id, file_dir, is_develop_mode):
    def _iterator():
        corpus_files = session.query(CorpusFile).filter(
            CorpusFile.corpus_id == corpus_id
        )

        for corpus_file in corpus_files:
            corpus = corpus_file.corpus

            for line in corpus_file.readline(file_dir):
                extracted = corpus.extract_data(line)
                result =  {
                    'corpus_data_id': ''.join([
                        corpus.corpus_id,
                        '{:0>8}'.format(extracted['id_in_corpus'])
                    ]),
                    'corpus_file_id':corpus_file.corpus_file_id,
                    'id_in_corpus': extracted['id_in_corpus'],
                    'text': extracted['text'],
                }
                LOGGER.info('proccess_file: ' + str(result['corpus_data_id']) + '  ' + result['text'][:20])
                yield result

    insert_stmt = mysql.insert(CorpusData)
    insert_stmt = insert_stmt.on_duplicate_key_update(
        corpus_file_id=insert_stmt.inserted.corpus_file_id,
        id_in_corpus=insert_stmt.inserted.id_in_corpus,
        text=insert_stmt.inserted.text,
        corpus_data_id=insert_stmt.inserted.corpus_data_id,
    )

    _bulk_insert(
        session,
        _iterator(),
        insert_stmt,
        LOGGER,
        is_develop_mode
    )
