import unittest
import pickle

from sanascan_backend.word import Word

from tests.use_lang_model import UseLangModel


class TestLangModel(UseLangModel):
    def setUp(self) -> None:
        self.lm = self.__class__.LM

    def test_score(self, msg: str = 'lm.scoreが何らかの値を返すか\'だけの\'テスト') -> None:
        words = [Word(surface='ホテル', yomi='ホテル')]
        self.lm.score(words)

    def test_vocab(
            self,
            msg: str = 'lm._get_word_setが何らかを返すか\'だけの\'テスト'
            ) -> None:
        self.lm._get_word_set()

    def test_pickle(self) -> None:
        pickle.dumps(self.lm)


if __name__ == '__main__':
    unittest.main()
