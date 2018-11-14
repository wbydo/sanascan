import unittest

from sanascan_backend.word import Word
from sanascan_backend.key import Key


class TestKey(unittest.TestCase):
    def setUp(self) -> None:
        self.hoge = Word(surface='歩下', yomi='ホゲ')
        self.fuga = Word(surface='不臥', yomi='フガ')

    def test_from_words(self) -> None:
        with self.subTest():
            k1 = Key.from_words([self.hoge])
            k2 = Key(5, 1)
            self.assertEqual(k1, k2)

        with self.subTest():
            k1 = Key.from_words([self.hoge, self.fuga])
            k2 = Key(5, 1, 5, 1)
            self.assertEqual(k1, k2)


if __name__ == '__main__':
    unittest.main()
