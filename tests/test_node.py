import unittest

from sanascan_backend.node import Node
from sanascan_backend.word import Word


class TestNode(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_init(self) -> None:
        with self.subTest():
            w = Word(surface='歩下', yomi='ホゲ')
            node = Node(w)
            self.assertEqual(node._word, w)

        with self.subTest():
            w = Word(surface='<s>', yomi='<s>')
            root_node = RootNode()
            self.assertEqual(root_node._word, w)


if __name__ == '__main__':
    unittest.main()
