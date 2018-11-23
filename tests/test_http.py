import unittest

from falcon import testing

from sanascan_backend.http import api


class TestHTTP(testing.TestCase):
    def setUp(self) -> None:
        super(self.__class__, self).setUp()
        self.api = api

    def test_post(self) -> None:
        result = self.simulate_post('/').json
        self.assertIn('id', result.keys())


if __name__ == '__main__':
    unittest.main()
