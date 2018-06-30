from logging import getLogger

import os
import hashlib

from .. import CorpusFile
from .. import SNKException

LOGGER = getLogger(__name__)

def insert(session, file_path, corpus_id):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * h.block_size), b''):
            h.update(chunk)
    checksum = h.hexdigest()

    target_file = CorpusFile(
        corpus_file_id=os.path.basename(file_path),
        checksum=checksum,
        corpus_id=corpus_id
    )

    LOGGER.info(f'name:\t\t{target_file.corpus_file_id}')
    LOGGER.info(f'checksum:\t{target_file.checksum}')
    LOGGER.info('')

    query = session.query(CorpusFile).filter(
        CorpusFile.corpus_file_id == target_file.corpus_file_id
    )
    exists = session.query(query.exists()).scalar()
    if not exists:
        n = target_file.corpus_file_id
        session.add(target_file)
        session.commit()

        LOGGER.info(f'{n}:\t格納完了!')
        LOGGER.info('')
    else:
        in_file = query.one()
        if not in_file.checksum == target_file.checksum:
            raise SNKException(
                f'DB:\t{in_file.corpus_file_id}\t{in_file.checksum}\n'+
                f'target:\t{target_file.corpus_file_id}\t{target_file.checksum}\n'+
                '一致しません!!!\n')
        else:
            LOGGER.info(f'{target_file.corpus_file_id}:\t格納済み!')
            LOGGER.info('')
