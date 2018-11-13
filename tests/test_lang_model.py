import unittest

from pathlib import Path

from sanascan_backend.lang_model import LangModel

class TestLangModel(unittest.TestCase):
    def setUp(self):
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
                self.lm = LangModel(f.read())

    def test_score(self, msg='lm.scoreが何らかの値を返すかテスト'):
        self.lm.score('歩下/ホゲ')

if __name__ == '__main__':
    unittest.main()
