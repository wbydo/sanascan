import unittest

from sanascan_backend.word import Word

class TestWord(unittest.TestCase):
    def test_from_str_of_singleword(self, msg: str ='Word#from_str_of_singleword') -> None:
        with self.subTest(msg='<unk>'):
            a = Word.from_str_of_singleword('<unk>')
            b = Word(surface='<unk>', yomi='<unk>')
            self.assertEqual(a, b)

        with self.subTest(msg='general case'):
            a = Word.from_str_of_singleword('歩下/ホゲ')
            b = Word(surface='歩下', yomi='ホゲ')
            self.assertEqual(a, b)

    def test_str(self, msg: str ='str(Word)') -> None:
        word = Word(surface='歩下', yomi='ホゲ')
        str_ = str(word)
        self.assertEqual(str_, '歩下/ホゲ')

    def test_static_to_str(self, msg: str='Word.to_str(words)') -> None:
        words = [
            Word(surface='歩下', yomi='ホゲ'),
            Word(surface='普が', yomi='フガ'),
            Word(surface='日余', yomi='ピヨ'),
        ]

        self.assertEqual(Word.to_str(words), '歩下/ホゲ 普が/フガ 日余/ピヨ')

if __name__ == '__main__':
    unittest.main()
