import unittest

from sanascan_backend.word import Word, TagWord
from sanascan_backend.evaluation.dp_matching import DPMatching


class TestDPMatching(unittest.TestCase):
    def test_dpmatching(self) -> None:
        ref = [
            Word('ホテル', 'ホテル'),
            Word('内', 'ナイ'),
            Word('の', 'ノ'),
            Word('飲食', 'インショク'),
            Word('店', 'テン'),
            Word('が', 'ガ'),
            Word('充実', 'ジュウジツ'),
            Word('し', 'シ'),
            Word('て', 'テ'),
            Word('おり', 'オリ'),
            Word('特に', 'トクニ'),
            TagWord('<num>'),
            TagWord('<eng>'),
            Word('の', 'ノ'),
            Word('バー', 'バー'),
            Word('は', 'ハ'),
            Word('重厚', 'ジュウコウ'),
            Word('な', 'ナ'),
            Word('インテリア', 'インテリア'),
            Word('で', 'デ'),
            Word('雰囲気', 'フンイキ'),
            Word('が', 'ガ'),
            Word('良く', 'ヨク'),
            Word('最高', 'サイコウ')
        ]

        est = [
            Word('ホテル', 'ホテル'),
            Word('内', 'ナイ'),
            Word('の', 'ノ'),
            Word('飲食', 'インショク'),
            Word('店', 'テン'),
            Word('が', 'ガ'),
            Word('充実', 'ジュウジツ'),
            Word('し', 'シ'),
            Word('て', 'テ'),
            Word('おり', 'オリ'),
            Word('特に', 'トクニ'),
            TagWord('<num>'),
            TagWord('<eng>'),
            Word('の', 'ノ'),
            Word('バー', 'バー'),
            Word('は', 'ハ'),
            Word('重厚', 'ジュウコウ'),
            Word('な', 'ナ'),
            Word('インテリア', 'インテリア'),
            Word('で', 'デ'),
            Word('雰囲気', 'フンイキ'),
            Word('が', 'ガ'),
            Word('良く', 'ヨク'),
            Word('最高', 'サイコウ')
        ]

        dpm = DPMatching(ref, est)

        self.fail(dpm.end_node.score)


if __name__ == '__main__':
    unittest.main()
