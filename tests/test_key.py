import unittest

from sanascan_backend.word import Word, TagWord
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

        with self.subTest(msg="all_of_subsequence（end=3と同等なはず）、順序も検査"):
            target = list(self.key.all_of_subsequence())
            wrong = [
                Key([2, 3]),
                Key([3]),
                Key([1, 2, 3]),
                Key([0, 1, 2, 3]),
            ]
            self.assertNotEqual(target, wrong)

            correct = [
                Key([3]),
                Key([2, 3]),
                Key([1, 2, 3]),
                Key([0, 1, 2, 3]),
            ]
            self.assertEqual(target, correct)

        with self.subTest(msg="TagWordが絡む場合、順序もざっと検査"):
            k = Key([3, 1, 4, TagWord('<num>')])
            target = list(k.all_of_subsequence())

            correct = [
                Key([TagWord('<num>')]),
                Key([4, TagWord('<num>')]),
                Key([1, 4, TagWord('<num>')]),
                Key([3, 1, 4, TagWord('<num>')]),
            ]
            self.assertEqual(target, correct)


if __name__ == '__main__':
    unittest.main()
