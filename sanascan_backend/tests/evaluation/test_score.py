import unittest

from sanascan_backend.evaluation.score import Score


class TestScore(unittest.TestCase):
    def test_template(self) -> None:
        s1 = Score(1, 2, 3, 4)
        s2 = Score(5, 6, 7, 8)
        s3 = Score(6, 8, 10, 12)
        self.assertEqual(s1 + s2, s3)


if __name__ == '__main__':
    unittest.main()
