from typing import ClassVar
from pathlib import Path
import unittest

from sanascan_backend.lang_model import LangModel


with (Path.home() / 'arpa/LM0006.txt').open() as f:
    LM = LangModel(f.read())

class UseLangModel(unittest.TestCase):
    LM = ClassVar[LangModel]

    @classmethod
    def setUpClass(klass) -> None:
        klass.LM = LM
