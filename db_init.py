import os
from sys import argv

from anakin.preprocess import util

if __name__ == '__main__':
    if len(argv) <= 1:
        raise ValueError('引数にdataディレクトリを指定')

    path = os.path.abspath(argv[1])
    util.register_single_file(path, 'rakuten_travel02_userReview')

    # util.insert_posts()
    # util.insert_posts(path)
    # util.insert_sentence(1000)
