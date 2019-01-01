import unittest

from sanascan_backend.node import Node, RootNode, EOSNode
from sanascan_backend.word import Word, TagWord

from tests.use_lang_model import UseLangModel


class TestNode(UseLangModel):
    def setUp(self) -> None:
        self.lm = self.__class__.LM

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
