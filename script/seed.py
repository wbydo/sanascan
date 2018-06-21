import os
import sys
import fnmatch

path_ = os.path.abspath(
    os.path.dirname(__file__))
sys.path.insert(0, path_)

import util

if __name__ == '__main__':
    # 楽天データに特化した処理を記載
    util.insert_corpus(
        '楽天データセット::楽天トラベル::ユーザレビュー',
        'RTUR',)

    session = util.Session()
    c = session.query(util.db.Corpus).one()
    session.close()

    for file_name in sorted(os.listdir(util.RAKUTEN_TRAVEL_DIR)):
        if fnmatch.fnmatch(file_name, 'travel02_userReview[0-9]*'):
            file_path = os.path.join(util.RAKUTEN_TRAVEL_DIR, file_name)
            util.insert_snkfile(file_path, c.id)

    util.insert_original_datum('RTUR', util.RAKUTEN_TRAVEL_DIR)
