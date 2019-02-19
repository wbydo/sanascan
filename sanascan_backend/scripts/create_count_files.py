from pathlib import Path
from shutil import copyfileobj

import yaml

from sanascan_backend.cejc.preprocess import create_wakati
from sanascan_backend.srilm import create_count_file

env_path = Path(__file__).parent.parent / ('env.yml')
with env_path.open() as f:
    env = yaml.load(f)

corpus_path = Path(env['cejc'])
for idx, p in enumerate(corpus_path.glob('data/**/*-morphSUW.csv')):
    if idx == 1:
        break

    wakati = create_wakati(p)
    count = create_count_file(wakati, 3, True)

    out = Path.home() / env['to_dir'] / (p.stem + '.count')
    with out.open('w') as f:
        copyfileobj(count, f)

    wakati.close()
    count.close()
