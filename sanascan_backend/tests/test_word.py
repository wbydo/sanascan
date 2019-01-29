import unittest
from natto import MeCab

from sanascan_backend.word import Word, TagWord
from sanascan_backend.word_builder import BuilderFromMeCab


class TestWord(unittest.TestCase):
    def test_from_str_of_singleword(
            self,
            msg: str = 'Word#from_str_of_singleword'
            ) -> None:

        with self.subTest(msg='<unk>'):
            a = Word.from_str_of_singleword('<unk>')
            b = Word(surface='<unk>', yomi='<unk>')
            self.assertNotEqual(a, b)

            b = TagWord('<unk>')
            self.assertEqual(a, b)

        with self.subTest(msg='general case'):
            a = Word.from_str_of_singleword('歩下/ホゲ')
            b = Word(surface='歩下', yomi='ホゲ')
            self.assertEqual(a, b)

    def test_str(self, msg: str = 'str(Word)') -> None:
        word = Word(surface='歩下', yomi='ホゲ')
        str_ = str(word)
        self.assertEqual(str_, '歩下/ホゲ')

    def test_static_to_str(self, msg: str = 'Word.to_str(words)') -> None:
        words = [
            Word(surface='歩下', yomi='ホゲ'),
            Word(surface='普が', yomi='フガ'),
            Word(surface='日余', yomi='ピヨ'),
        ]

        self.assertEqual(Word.to_str(words), '歩下普が日余')

    def test_eq(self) -> None:
        self.assertNotEqual(
            Word(surface='<unk>', yomi='<unk>'),
            TagWord('<unk>')
        )

    def test_from_sentence(self) -> None:
        r1 = list(BuilderFromMeCab.from_sentence(
            'ホテル内の飲食店が充実しており、特に１Ｆのバーは重厚なインテリアで、雰囲気が良く最高',
            MeCab()
        ))

        r2 = [
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
        self.assertEqual(r1, r2)

    def test_tag_word(self) -> None:
        TagWord('<unk>')
        with self.assertRaises(ValueError):
            TagWord('hoge')


if __name__ == '__main__':
    unittest.main()
