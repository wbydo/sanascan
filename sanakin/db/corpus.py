from .. import SNKException

def _extract_data(corpus_symbol):
    if not corpus_symbol == 'RTUR':
        raise SNKException(
            f'symbol: {corpus_symbol}')
    return _rakuten_travel_user_review

def _rakuten_travel_user_review(line):
    tsv = line.split('\t')
    return {
        'id_in_corpus': int(tsv[3]),
        'contents': tsv[2].strip()}
