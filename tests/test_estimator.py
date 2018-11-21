import unittest
from pathlib import Path

from natto import MeCab

from sanascan_backend.estimator import Estimator
from sanascan_backend.lang_model import LangModel
from sanascan_backend.word import Word
from sanascan_backend.key import Key


class TestEstimator(unittest.TestCase):
    def setUp(self) -> None:
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self.lm = LangModel(f.read())

    def test_estimate(self) -> None:
        # sentence = 'ホテル内の飲食店が充実しており、特に１Ｆのバーは重厚なインテリアで、雰囲気が良く最高'
        sentence = '特に１Ｆのバーは最高'

        test_words = list(Word.from_sentence(sentence, MeCab()))
        key = Key.from_words(test_words)

        estimator = Estimator(self.lm)
        for k in key:
            estimator.add(k)
        estimator.finish()

        result = estimator.result
        self.assertEqual(test_words, result)


if __name__ == '__main__':
    unittest.main()
