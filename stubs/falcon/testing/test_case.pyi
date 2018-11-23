import unittest

from .client import TestClient

class TestCase(unittest.TestCase, TestClient): ...
