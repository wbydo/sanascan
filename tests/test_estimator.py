import unittest
from pathlib import Path

from sanascan_backend.word import Word
from sanascan_backend.estimator import estimate
from sanascan_backend.lang_model import LangModel
from sanascan_backend.key_to_word_map import KeyToWordMap


class TestEstimator(unittest.TestCase):
    def setUp(self) -> None:
        self.words = [
            Word('ホテル', 'ホテル'),
            Word('内', 'ナイ'),
            Word('の', 'ノ'),
            Word('飲食', 'インショク'),
            Word('店', 'テン'),
            Word('が', 'ガ'),
            Word('充実', 'ジュウジツ'),
            Word('し', 'シ'),
            Word('て', 'テ'),
            Word('おり', 'オリ'),
            Word('特に', 'トクニ'),
            Word('<num>', '<num>'),
            Word('<eng>', '<eng>'),
            Word('の', 'ノ'),
            Word('バー', 'バー'),
            Word('は', 'ハ'),
            Word('重厚', 'ジュウコウ'),
            Word('な', 'ナ'),
            Word('インテリア', 'インテリア'),
            Word('で', 'デ'),
            Word('雰囲気', 'フンイキ'),
            Word('が', 'ガ'),
            Word('良く', 'ヨク'),
            Word('最高', 'サイコウ')
        ]

        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self.lm = LangModel(f.read())

    def test_hoge(self) -> None:
        result = estimate(
            self.words,
            KeyToWordMap(self.lm.get_vocab()),
            self.lm,
            self.lm._order
        )
        print(result)


if __name__ == '__main__':
    unittest.main()
