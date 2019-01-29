from pathlib import Path
import pandas as pd
import yaml

from sanascan_backend.parser.cejc import CEJC


path = Path(__file__).parent / ('env.yml')
with path.open() as f:
    csv_path = yaml.load(f)['cejc']
    df = pd.read_csv(csv_path, encoding='shift-jis')

parser = CEJC()
result = parser(df)
for s in result.value:
    if len(s.words) != 0:
        print(s)
