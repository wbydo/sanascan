import os
from sys import argv

from anakin.preprocess import util

if __name__ == '__main__':
    if len(argv) <= 1:
        raise ValueError('引数にdataディレクトリを指定')

    path = os.path.abspath(argv[1])
    util.insert_files(path)
    util.insert_posts(path)
    util.insert_sentence(1000)
