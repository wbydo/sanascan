import os
from sys import argv

import glob

from anakin.preprocess import util
from anakin.preprocess.dataset import Dataset

if __name__ == '__main__':
    if len(argv) <= 1:
        raise ValueError('引数にdataディレクトリを指定')

    path = os.path.abspath(argv[1])
    p = os.path.join(path, '*')
    for f in glob.iglob(p):
        util.register_single_file(f, Dataset.RTUR)
