import os
import sys
import fnmatch

path_ = os.path.abspath(
    os.path.dirname(__file__))
sys.path.insert(0, path_)

import util

if __name__ == '__main__':
    util.insert_splitter('Splitter001')
