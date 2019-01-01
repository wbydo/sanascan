from sanascan_backend.word import TagWord
from sanascan_backend.key import Key

from tests.use_lang_model import UseLangModel


class TestVocabulary(UseLangModel):
    def setUp(self) -> None:
        self.lm = self.__class__.LM
        self.vocab = self.lm.create_vocabrary()
        self.key = Key([3, 1, 4, TagWord('<num>')])
        self.keys = [
            Key([TagWord('<num>')]),
            Key([4, TagWord('<num>')]),
            Key([1, 4, TagWord('<num>')]),
            Key([3, 1, 4, TagWord('<num>')]),
        ]

    def test_have_num_tagword(self) -> None:
        with self.subTest():
            self.assertIn(TagWord('<num>'), self.lm._get_word_set())

        self.assertIn(Key([TagWord('<num>')]), self.vocab._datum.keys())

    def test_get_by_key(self) -> None:
        self.assertNotEqual(
            list(self.vocab.get_by_key(self.key)),
            []
        )
        for word, key in self.vocab.get_by_key(self.key):
            self.assertIn(key, self.keys)
