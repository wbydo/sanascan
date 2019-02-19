from typing import ClassVar, TypeVar, Type
from pathlib import Path
import unittest

from sanascan_backend.lang_model import LangModel

path = (Path.home() / 'arpa/LM0006.txt').resolve()
with path.open('r') as f:
    LM = LangModel(f)

T = TypeVar('T', bound='UseLangModel')


class UseLangModel(unittest.TestCase):
    LM = ClassVar[LangModel]

    @classmethod
    def setUpClass(klass: Type[T]) -> None:
        klass.LM = LM
