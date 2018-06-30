from ..err import SNKException

class BaseCorpus:
    def _extract_function(self, corpus_id):
        if not corpus_id == 'CPRTUR':
            raise SNKException(
                f'symbol: {corpus_id}')
        return self._rakuten_travel_user_review

    def _rakuten_travel_user_review(self, line):
        tsv = line.split('\t')
        return {
            'id_in_corpus': int(tsv[3]),
            'text': tsv[2].strip()}
