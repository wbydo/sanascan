import unittest

from sanascan_backend.word import Word
from sanascan_backend.evaluation.dp_matching import DPMatching
from sanascan_backend.evaluation.score import Score


class TestDPMatching(unittest.TestCase):
    def test_dpmatching(self) -> None:
        with self.subTest('correct'):
            ref = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('の', 'ノ'),
                Word('飲食', 'インショク'),
                Word('店', 'テン'),
                Word('が', 'ガ'),
            ]

            est = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('の', 'ノ'),
                Word('飲食', 'インショク'),
                Word('店', 'テン'),
                Word('が', 'ガ'),
            ]

            dpm = DPMatching(ref, est)

            s = Score(correct=6)
            self.assertEqual(dpm.end_node.score, s)

        with self.subTest('dropout'):
            ref = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('の', 'ノ'),
                Word('飲食', 'インショク'),
                Word('店', 'テン'),
                Word('が', 'ガ'),
            ]

            est = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('飲食', 'インショク'),
                Word('店', 'テン'),
                Word('が', 'ガ'),
            ]

            dpm = DPMatching(ref, est)

            s = Score(correct=5, dropout=1)
            self.assertEqual(dpm.end_node.score, s)

        with self.subTest('insert'):
            ref = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('の', 'ノ'),
                Word('飲食', 'インショク'),
                Word('店', 'テン'),
                Word('が', 'ガ'),
            ]

            est = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('の', 'ノ'),
                Word('飲食', 'インショク'),
                Word('飲食', 'インショク'),
                Word('店', 'テン'),
                Word('が', 'ガ'),
            ]

            dpm = DPMatching(ref, est)

            s = Score(correct=6, insert=1)
            self.assertEqual(dpm.end_node.score, s)

        with self.subTest('substitute'):
            ref = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('の', 'ノ'),
                Word('飲食', 'インショク'),
                Word('店', 'テン'),
                Word('が', 'ガ'),
            ]

            est = [
                Word('ホテル', 'ホテル'),
                Word('内', 'ナイ'),
                Word('の', 'ノ'),
                Word('飲食', 'インショク'),
                Word('さん', 'サン'),
                Word('が', 'ガ'),
            ]

            dpm = DPMatching(ref, est)

            s = Score(correct=5, substitute=1)
            self.assertEqual(dpm.end_node.score, s)


if __name__ == '__main__':
    unittest.main()
