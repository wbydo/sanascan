import unittest

from falcon import testing
from natto import MeCab

from sanascan_backend.http import api
from sanascan_backend.word import Word
from sanascan_backend.key import Key
from sanascan_backend.yomi_property import ColNum, Position
from sanascan_backend.word_builder import BuilderFromMeCab


class TestHTTP(testing.TestCase):
    def setUp(self) -> None:
        super(self.__class__, self).setUp()
        self.api = api

    def test_http_estimate(self) -> None:

        for mode, t in zip(['normal', 'proposal'], [Position, ColNum]):
            with self.subTest(f'{mode}の場合'):
                resp = self.simulate_post('/').json
                self.assertIn('eid', resp.keys())
                eid = resp['eid']

                sentence = '特に１Ｆのバーは最高'
                test_words = list(
                    BuilderFromMeCab.from_sentence(sentence, MeCab())
                )
                key = Key.from_words(test_words, t)

                for k in key:
                    params = {
                        'key': str(k),
                        'mode': mode
                    }
                    result = self.simulate_post(f'/{eid}', params=params)
                    self.assertLess(result.status_code, 400)

                get_result = self.simulate_get(f'/{eid}')
                self.assertLess(get_result.status_code, 400)

                correct = Word.to_str(test_words)
                self.assertEqual(correct, get_result.json['result'])


if __name__ == '__main__':
    unittest.main()
