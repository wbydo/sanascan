import unittest

from sanascan_backend.word import Word, TagWord
from sanascan_backend.key import Key
from sanascan_backend.yomi_property import ColNum, Position


class TestKey(unittest.TestCase):
    def setUp(self) -> None:
        self.hoge = Word(surface='歩下', yomi='ホゲ')
        self.fuga = Word(surface='不臥', yomi='フガ')

        self.key = Key.from_int([0, 1, 2, 3])

    def test_from_words_by_colnum(self) -> None:
        with self.subTest():
            k1 = Key.from_words([self.hoge], ColNum)
            k2 = Key.from_int([5, 1])
            self.assertEqual(k1, k2)

        with self.subTest():
            k1 = Key.from_words([self.hoge, self.fuga], ColNum)
            k2 = Key.from_int([5, 1, 5, 1])
            self.assertEqual(k1, k2)

    def test_from_words_by_position(self) -> None:
        with self.subTest():
            k1 = Key.from_words([self.hoge], Position)
            k2 = Key.from_str(['ホ', 'ケ'])
            self.assertEqual(k1, k2)

        with self.subTest():
            k1 = Key.from_words([self.hoge, self.fuga], Position)
            k2 = Key.from_str(['ホ', 'ケ', 'フ', 'カ'])
            self.assertEqual(k1, k2)

    def test_str(self) -> None:
        k = Key.from_int([1])
        self.assertEqual(str(k), '1')

        k = Key.from_int([0, 1])
        with self.assertRaises(TypeError):
            str(k)

    def test_add(self) -> None:
        k1 = Key.from_int([0, 1, TagWord('<num>')])
        k2 = Key.from_int([2, 3])
        self.assertEqual(
            k1 + k2,
            Key.from_int([0, 1, TagWord('<num>'), 2, 3])
        )

    def test_subsequence(self) -> None:
        with self.subTest(msg="end=4でerror"):
            with self.assertRaises(ValueError):
                list(self.key.subsequence_with_end(4))

        with self.subTest(msg="end<0でerror"):
            with self.assertRaises(ValueError):
                list(self.key.subsequence_with_end(-1))

        with self.subTest(msg="end=2"):
            list_ = list(self.key.subsequence_with_end(2))
            self.assertIn(Key.from_int([2]), list_)
            self.assertIn(Key.from_int([1, 2]), list_)
            self.assertIn(Key.from_int([0, 1, 2]), list_)

        with self.subTest(msg="all_of_subsequence（end=3と同等なはず）、順序も検査"):
            target = list(self.key.all_of_subsequence())
            wrong = [
                Key.from_int([2, 3]),
                Key.from_int([3]),
                Key.from_int([1, 2, 3]),
                Key.from_int([0, 1, 2, 3]),
            ]
            self.assertNotEqual(target, wrong)

            correct = [
                Key.from_int([3]),
                Key.from_int([2, 3]),
                Key.from_int([1, 2, 3]),
                Key.from_int([0, 1, 2, 3]),
            ]
            self.assertEqual(target, correct)

        with self.subTest(msg="TagWordが絡む場合、順序もざっと検査"):
            k = Key.from_int([3, 1, 4, TagWord('<num>')])
            target = list(k.all_of_subsequence())

            correct = [
                Key.from_int([TagWord('<num>')]),
                Key.from_int([4, TagWord('<num>')]),
                Key.from_int([1, 4, TagWord('<num>')]),
                Key.from_int([3, 1, 4, TagWord('<num>')]),
            ]
            self.assertEqual(target, correct)


if __name__ == '__main__':
    unittest.main()
