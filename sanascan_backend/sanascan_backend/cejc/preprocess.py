from typing import IO

from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd

from .parser import CEJC


def create_wakati(csv_path: Path) -> IO[str]:
    df = pd.read_csv(csv_path, encoding='shift-jis')
    out = NamedTemporaryFile('wt+', encoding='utf-8')

    parser = CEJC()
    result = parser(df)
    for s in result.value:
        if len(s.words) != 0:
            print(s, file=out)

    out.seek(0)
    return out
