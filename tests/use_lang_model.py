from typing import ClassVar
from pathlib import Path
import unittest

from sanascan_backend.lang_model import LangModel

path = (Path.home() / 'arpa/LM0006.txt').resolve()
with path.open('r') as f:
    LM = LangModel(f)


class UseLangModel(unittest.TestCase):
    LM = ClassVar[LangModel]

    @classmethod
    def setUpClass(klass) -> None:
        klass.LM = LM
