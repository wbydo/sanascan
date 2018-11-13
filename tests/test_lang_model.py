import unittest

from pathlib import Path

from sanascan_backend.lang_model import LangModel
from sanascan_backend.word import Word


@unittest.skip("一時スキップ")
class TestLangModel(unittest.TestCase):
    def setUp(self) -> None:
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
                self.lm = LangModel(f.read())

    def test_score(self, msg: str = 'lm.scoreが何らかの値を返すか\'だけの\'テスト') -> None:
        words = [Word(surface='ホテル', yomi='ホテル')]
        self.lm.score(words)

    def test_vocab(self, msg: str = 'lm.get_vocabが何らかを返すか\'だけの\'テスト') -> None:
        self.lm.get_vocab()


if __name__ == '__main__':
    unittest.main()
