from typing import cast

import unittest

from natto import MeCab

from sanascan_backend.estimator import Estimator
from sanascan_backend.word import TagWord, Sentence
from sanascan_backend.key import Key
from sanascan_backend.yomi_property import ColNum, Position
from sanascan_backend.word_builder import BuilderFromMeCab
from sanascan_backend.lang_model import LangModel


from tests.use_lang_model import UseLangModel


class TestEstimator(UseLangModel):
    lm: LangModel

    def setUp(self) -> None:
        self.lm = cast(LangModel, self.LM)

    def test_estimate(self) -> None:
        # sentence = 'ホテル内の飲食店が充実しており、特に１Ｆのバーは重厚なインテリアで、雰囲気が良く最高'
        text = '特に１Ｆのバーは最高'

        words = list(BuilderFromMeCab.from_plaintext(text, MeCab()))
        sentence = Sentence.from_iter(words)

        for t in [ColNum, Position]:
            with self.subTest(f'{t}の場合'):
                key = Key.from_sentence(sentence, t)

                estimator = Estimator(self.lm)
                for k in key:
                    estimator.add(k)
                estimator.finish()

                with self.subTest("答えが正しい"):
                    result = estimator.result
                    assert result is not None
                    self.assertEqual(sentence.words, tuple(result))

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
