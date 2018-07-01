import os
import sys

from natto import MeCab

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

import sanakin.morphological_analysis.cli as manalysis
from sanakin.cli_util import SNKCLIEngine

# ロガー設定
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger().setLevel(logging.INFO)

def delete_mode(session):
    pass

def sandbox_mode(session):
    pass

def insert_mode(session, *, is_develop_mode=True):
    with MeCab() as mecab:
        manalysis.insert(session, mecab, True)

if __name__ == '__main__':
    cli = SNKCLIEngine(
            description='''\

                !!! 形態素解析用のスクリプトだぞ !!!

                DBに形態素解析結果を投入するためのCLI。
                引数なしで実行した場合、100件だけやる。\
            ''',
    )

    cli.delete_mode = delete_mode
    cli.sandbox_mode = sandbox_mode
    cli.insert_mode = insert_mode
    cli.run()
