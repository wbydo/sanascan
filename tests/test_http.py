import unittest

from falcon import testing

from sanascan_backend.http import api


class TestHTTP(testing.TestCase):
    def setUp(self) -> None:
        super(self.__class__, self).setUp()
        self.api = api

    def test_hello(self) -> None:
        result = self.simulate_get('/')
        d = {'hello': 'world'}
        self.assertEqual(result.json, d)


if __name__ == '__main__':
    unittest.main()
