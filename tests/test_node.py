import unittest
from pathlib import Path

from sanascan_backend.node import Node, RootNode, EOSNode
from sanascan_backend.word import Word, TagWord
from sanascan_backend.lang_model import LangModel


class TestNode(unittest.TestCase):
    def setUp(self) -> None:
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self.lm = LangModel(f.read())

        self.hoge_word = Word(surface='特に', yomi='トクニ')
        self.root = RootNode()
        self.node = Node(self.hoge_word, [self.root], self.lm)
        self.eos = EOSNode([self.node], self.lm)

    def test_init(self) -> None:
        with self.subTest():
            self.assertEqual(self.node._word, self.hoge_word)

        with self.subTest():
            w = TagWord('<s>')
            self.assertEqual(self.root._word, w)

        with self.subTest():
            w = TagWord('</s>')
            self.assertEqual(self.eos._word, w)


if __name__ == '__main__':
    unittest.main()
