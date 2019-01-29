import unittest

from pathlib import Path
import pandas as pd
import yaml

from sanascan_backend.parser.cejc import SOS
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
            self.assertIsInstance(result.value, pd.Series)
            self.assertEqual(result.value['文頭フラグ'], 'B')

        with self.subTest('error'):
            with self.assertRaises(ParseError) as cm:
                parser(df.iloc[2:, :])

            e = cm.exception
            self.assertIsInstance(e.next, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
