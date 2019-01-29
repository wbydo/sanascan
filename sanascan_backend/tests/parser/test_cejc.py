import unittest

from pathlib import Path
import pandas as pd
import yaml

from sanascan_backend.word import Word, Sentence
from sanascan_backend.parser.cejc import SOS, SentenceParser, CEJC
from wbydo_parser.base import ParseError

path = Path(__file__).parent.parent.parent / ('env.yml')
with path.open() as f:
    csv_path = yaml.load(f)['cejc']
    df = pd.read_csv(csv_path, encoding='shift-jis')


class TestCEJC(unittest.TestCase):
    def test_sos(self) -> None:
        parser = SOS()

        with self.subTest('success'):
            result = parser(df)
            self.assertIsInstance(result.value, Word)

        with self.subTest('error'):
            with self.assertRaises(ParseError) as cm:
                parser(df.iloc[2:, :])

            e = cm.exception
            self.assertIsInstance(e.next, pd.DataFrame)

    def test_sentence(self) -> None:
        parser = SentenceParser()
        result = parser(df.iloc[1:, :])
        self.assertEqual(len(result.value.words), 8)

    def test_cejc(self) -> None:
        parser = CEJC()
        result = parser(df)
        for s in result.value:
            self.assertIsInstance(s, Sentence)


if __name__ == '__main__':
    unittest.main()
