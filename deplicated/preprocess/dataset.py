import enum
import re

from collections import namedtuple

DatasetAttribute = namedtuple('DatasetAttribute', ['formal_name', 'extractor'])

def _rakuten_travel_user_review(contents):
    # !!変更には注意!!
    # DBで管理されているので変更するなら新しいenum作ること

    # 大きなバイナリを一気にdecodeが不安
    # メモリリークしたら逐次処理を考える
    for line in contents.decode('utf-8').strip().split('\n'):
        tsv = line.split('\t')
        contents = tsv[2].strip()
        id = int(tsv[3])
        yield {'id':id, 'contents':contents}

@enum.unique
class Dataset(enum.Enum):
    RTUR = DatasetAttribute(
        formal_name='Rakuten_travel02_userReview',
        extractor=_rakuten_travel_user_review
    )
