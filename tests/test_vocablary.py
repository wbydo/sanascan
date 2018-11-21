import unittest

from pathlib import Path

from sanascan_backend.lang_model import LangModel
from sanascan_backend.vocabulary import Vocabulary
from sanascan_backend.word import TagWord
from sanascan_backend.key import Key


class TestVocabulary(unittest.TestCase):
    def setUp(self) -> None:
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self.lm = LangModel(f.read())
        self.vocab = Vocabulary(self.lm.get_vocab())
        self.key = Key([3, 1, 4, TagWord('<num>')])
        self.keys = [
            Key([TagWord('<num>')]),
            Key([4, TagWord('<num>')]),
            Key([1, 4, TagWord('<num>')]),
            Key([3, 1, 4, TagWord('<num>')]),
        ]

    def test_have_num_tagword(self) -> None:
        with self.subTest():
            self.assertIn(TagWord('<num>'), self.lm.get_vocab())

        self.assertIn(Key([TagWord('<num>')]), self.vocab._datum.keys())

    def test_get_by_key(self) -> None:
        self.assertNotEqual(
            list(self.vocab.get_by_key(self.key, 3)),
            []
        )
        for word, key in self.vocab.get_by_key(self.key, 3):
            self.assertIn(key, self.keys)
