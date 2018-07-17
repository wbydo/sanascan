from ..snksession import SNKSession

from logging import getLogger

LOGGER = getLogger(__name__)

class BaseCorpusData:
    @classmethod
    def create_iter(klass, corpus_file, dir_):
        '''
        Args:
            corpus_file[sanakin.CorpusFile]:
            dir_[pathlib.Path]
        '''

        with SNKSession() as session:
            corpus_file = session.merge(corpus_file)
            corpus = corpus_file.corpus

            for line in corpus_file.readline(dir_):
                extracted = corpus.extract_data(line)
                k = klass(
                    corpus_data_id=''.join([
                        corpus.corpus_id,
                        '{:0>8}'.format(extracted['id_in_corpus'])
                    ]),
                    corpus_file_id=corpus_file.corpus_file_id,
                    id_in_corpus=extracted['id_in_corpus'],
                    text=extracted['text'],
                )
                LOGGER.info('proccess_file: ' + k.corpus_data_id + '  ' + k.text[:20])
                yield k
