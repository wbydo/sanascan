from logging import getLogger
import sys

import sqlalchemy.dialects.mysql as mysql

from .. import Corpus, CorpusData

from ..cli_const import INSERT_CORPUS_DATA_NUM

LOGGER = getLogger(__name__)

def insert(session, engine, corpus_id, file_dir, is_develop_mode):
    def process_all_line():
        corpus = session.query(Corpus).filter(
            Corpus.corpus_id == corpus_id
        ).one()

        corpus_files = corpus.corpus_files

        i = 0
        for corpus_file in corpus_files:
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
                i+=1
                if is_develop_mode and i >= INSERT_CORPUS_DATA_NUM:
                    raise StopIteration()

    def insert_(corpus_datam):
        insert_stmt = mysql.insert(CorpusData)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            corpus_file_id=insert_stmt.inserted.corpus_file_id,
            id_in_corpus=insert_stmt.inserted.id_in_corpus,
            text=insert_stmt.inserted.text,
            corpus_data_id=insert_stmt.inserted.corpus_data_id,
        )
        with engine.begin() as conn:
            conn.execute(on_duplicate_key_stmt, datum)

    datum = []
    max_size = 500_000_000
    for d in process_all_line():
        if sys.getsizeof(datum) < max_size:
            datum.append(d)
        else:
            LOGGER.info(f'INSERT: {len(datum)}件挿入!!!')
            insert_(datum)
            datum = []
    if datum:
        LOGGER.info(f'INSERT: {len(datum)}件挿入!!!')
        insert_(datum)
    session.commit()
