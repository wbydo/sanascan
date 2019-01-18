from sanascan_backend.word import TagWord
from sanascan_backend.key import Key

from tests.use_lang_model import UseLangModel


class TestVocabulary(UseLangModel):
    def setUp(self) -> None:
        self.lm = self.__class__.LM
        self.vocab = self.lm.create_vocabrary()
        self.key = Key.from_int([3, 1, 4, TagWord('<num>')])
        self.keys = [
            Key.from_int([TagWord('<num>')]),
            Key.from_int([4, TagWord('<num>')]),
            Key.from_int([1, 4, TagWord('<num>')]),
            Key.from_int([3, 1, 4, TagWord('<num>')]),
        ]

    def test_have_num_tagword(self) -> None:
        with self.subTest():
            self.assertIn(TagWord('<num>'), self.lm._get_word_set())

        self.assertIn(
            Key.from_int([TagWord('<num>')]),
            self.vocab._datum.keys()
        )

    def test_get_by_key(self) -> None:
        self.assertNotEqual(
            list(self.vocab.get_by_key(self.key)),
            []
        )
        for word, key in self.vocab.get_by_key(self.key):
            self.assertIn(key, self.keys)
