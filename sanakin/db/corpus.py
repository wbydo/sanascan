from .. import SNKException

def _extract_data(corpus_id):
    if not corpus_id == 'RTUR':
        raise SNKException(
            f'symbol: {corpus_id}')
    return _rakuten_travel_user_review

def _rakuten_travel_user_review(line):
    tsv = line.split('\t')
    return {
        'id_in_corpus': int(tsv[3]),
        'text': tsv[2].strip()}
