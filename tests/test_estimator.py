import unittest
from pathlib import Path

from natto import MeCab

from sanascan_backend.estimator import estimate
from sanascan_backend.lang_model import LangModel
from sanascan_backend.word import Word


class TestEstimator(unittest.TestCase):
    def setUp(self) -> None:
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self.lm = LangModel(f.read())

    def test_estimate(self) -> None:
        # sentence = 'ホテル内の飲食店が充実しており、特に１Ｆのバーは重厚なインテリアで、雰囲気が良く最高'
        sentence = '特に１Ｆのバーは最高'

        words = Word.from_sentence(sentence, MeCab())
        result = estimate(
            words,
            self.lm,
        )

        correct = '特に/トクニ <num>/<num> <eng>/<eng> の/ノ バー/バー は/ハ 最高/サイコウ'
        self.assertEqual(Word.to_str(result), correct)


if __name__ == '__main__':
    unittest.main()
