from sanakin_db.util import init
from pathlib import Path
import yaml

from sanakin_db import Sentence, SNKSession

with (Path() / 'config.yml').open() as f:
    d = yaml.load(f.read())
    init(**d['localhost'])

with SNKSession() as session:
    for s in session.query(Sentence).limit(100):
        print(s.text)
