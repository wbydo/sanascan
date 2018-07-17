from logging import getLogger

import hashlib

LOGGER = getLogger(__name__)

class BaseCorpusFile:
    @classmethod
    def create(klass, file_path):
        '''
        Args:
            file_path(pathlib.Path): File path
        '''
        h = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(2048 * h.block_size), b''):
                h.update(chunk)
        checksum = h.hexdigest()

        k = klass(checksum=checksum, corpus_file_id=file_path.name)
        LOGGER.info(k)
        return k

    def _readline(self, file_path):
        with open(file_path) as f:
            for line in iter(f.readline, ''):
                yield line.strip()
