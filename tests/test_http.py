import unittest

from falcon import testing
from natto import MeCab

from sanascan_backend.http import api
from sanascan_backend.word import Word
from sanascan_backend.key import Key


class TestHTTP(testing.TestCase):
    def setUp(self) -> None:
        super(self.__class__, self).setUp()
        self.api = api

    def test_http_estimate(self) -> None:
        post_result = self.simulate_post('/').json
        self.assertIn('id', post_result.keys())
        id_ = post_result['id']

        sentence = '特に１Ｆのバーは最高'
        test_words = list(Word.from_sentence(sentence, MeCab()))
        key = Key.from_words(test_words)

        for k in key:
            params = {
                'id': id_,
                'key': str(k)
            }
            result = self.simulate_put('/', params=params)
            self.assertLess(result.status_code, 400)

        get_result = self.simulate_get('/', params={'id': id_})
        self.assertLess(get_result.status_code, 400)

        correct = Word.to_str(test_words)
        self.assertEqual(correct, get_result.json['result'])


if __name__ == '__main__':
    unittest.main()
