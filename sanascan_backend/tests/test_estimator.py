import unittest

from natto import MeCab

from sanascan_backend.estimator import Estimator
from sanascan_backend.word import TagWord
from sanascan_backend.key import Key
from sanascan_backend.yomi_property import ColNum, Position
from sanascan_backend.word_builder import AnalyzeByMeCab


from tests.use_lang_model import UseLangModel


class TestEstimator(UseLangModel):
    def setUp(self) -> None:
        self.lm = self.__class__.LM

    def test_estimate(self) -> None:
        # sentence = 'ホテル内の飲食店が充実しており、特に１Ｆのバーは重厚なインテリアで、雰囲気が良く最高'
        sentence = '特に１Ｆのバーは最高'

        test_words = list(AnalyzeByMeCab.from_sentence(sentence, MeCab()))

        for t in [ColNum, Position]:
            with self.subTest(f'{t}の場合'):
                key = Key.from_words(test_words, t)

                estimator = Estimator(self.lm)
                for k in key:
                    estimator.add(k)
                estimator.finish()

                with self.subTest("答えが正しい"):
                    result = estimator.result
                    self.assertEqual(test_words, result)

                with self.subTest("リセットがちゃんときく"):
                    estimator.reset()
                    self.assertEqual(len(estimator.wait_child), 1)

    def test_add_side_effect(
            self,
            msg: str = "addの副作用がちゃんと機能する"
            ) -> None:
        est = Estimator(self.lm)
        est.add(Key([0]))

        with self.subTest():
            self.assertEqual(len(est.wait_child), 2)

        with self.subTest():
            self.assertEqual(
                est.key,
                Key([TagWord('<s>'), 0])
            )


if __name__ == '__main__':
    unittest.main()
