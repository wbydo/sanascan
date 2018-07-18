from logging import getLogger

from ..snksession import SNKSession

LOGGER = getLogger(__name__)

class BaseSentence:
    @classmethod
    def create_iter(klass, corpus_data, sentence_delimiter):
        '''
        Args:
            corpus_data[sanakin.CorpusData]:
            sentence_delimiter[sanakin.SentenceDelimiter]:
        '''

        data = corpus_data
        delimiter = sentence_delimiter

        for sentence in sentence_delimiter.split(corpus_data.text):
            k = klass(
                corpus_data_id=data.corpus_data_id,
                sentence_id='{}_{}_{:0>2}{:0>2}'.format(
                    data.corpus_data_id,
                    delimiter.sentence_delimiter_id,
                    sentence['length'],
                    sentence['nth']
                ),
                **sentence
            )

            LOGGER.info('{}:\t{}'.format(
                k.sentence_id,
                k.text,
            ))

            yield k
