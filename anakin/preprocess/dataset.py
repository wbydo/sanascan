import enum
import re
import jaconv

from collections import namedtuple

DatasetAttribute = namedtuple('DatasetAttribute', ['formal_name', 'strategy'])

def _rakuten_travel_user_review(contents):
    # 大きなバイナリを一気にdecodeが不安
    # メモリリークしたら逐次処理を考える
    for line in iter(contents.decode('utf-8').split()):
        tsv = line.split('\t')
        contents = tsv[2].strip()
        id = int(tsv[3])
        yield {'id':id, 'contents':contents}

@enum.unique
class Dataset(enum.Enum):
    RTUR = DatasetAttribute(
        formal_name='Rakuten_travel02_userReview',
        strategy=_rakuten_travel_user_review
    )
