import unittest

from pathlib import Path

from sanascan_backend.lang_model import LangModel

class TestLangModel(unittest.TestCase):
    def setUp(self):
        with (Path.home() / 'arpa/LM0006.txt').open() as f:
            self.lm = LangModel(f.read())

    @unittest.skip("一時skip")
    def test_getvocab(self):
        self.lm.get_vocab()

if __name__ == '__main__':
    unittest.main()
