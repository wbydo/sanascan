import unittest

from pathlib import Path

from sanascan_backend.lang_model import LangModel
from sanascan_backend.word import Word

class TestLangModel(unittest.TestCase):
    def setUp(self) -> None:
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
                self.lm = LangModel(f.read())

    def test_score(self, msg: str='lm.scoreが何らかの値を返すかテスト') -> None:
        words = [Word(surface='歩下', yomi='ホゲ')]
        self.lm.score(words)

if __name__ == '__main__':
    unittest.main()
