import unittest

from sanascan_backend.word import Word
from sanascan_backend.key import Key


class TestKey(unittest.TestCase):
    def setUp(self) -> None:
        self.hoge = Word(surface='歩下', yomi='ホゲ')
        self.fuga = Word(surface='不臥', yomi='フガ')

        self.key = Key([0, 1, 2, 3])

    def test_from_words(self) -> None:
        with self.subTest():
            k1 = Key.from_words([self.hoge])
            k2 = Key([5, 1])
            self.assertEqual(k1, k2)

        with self.subTest():
            k1 = Key.from_words([self.hoge, self.fuga])
            k2 = Key([5, 1, 5, 1])
            self.assertEqual(k1, k2)

    def test_subsequence(self) -> None:
        with self.subTest(msg="end=4でerror"):
            with self.assertRaises(ValueError):
                list(self.key.subsequence_with_end(4))

        with self.subTest(msg="end<0でerror"):
            with self.assertRaises(ValueError):
                list(self.key.subsequence_with_end(-1))

        with self.subTest(msg="end=2"):
            list_ = list(self.key.subsequence_with_end(2))
            self.assertIn(Key([2]), list_)
            self.assertIn(Key([1, 2]), list_)
            self.assertIn(Key([0, 1, 2]), list_)

        with self.subTest(msg="all_of_subsequence（end=3と同等なはず）"):
            list_ = list(self.key.all_of_subsequence())
            self.assertIn(Key([3]), list_)
            self.assertIn(Key([2, 3]), list_)
            self.assertIn(Key([1, 2, 3]), list_)
            self.assertIn(Key([0, 1, 2, 3]), list_)

        with self.subTest(msg="end=の場合"):
            pass


if __name__ == '__main__':
    unittest.main()
