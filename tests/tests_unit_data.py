import unittest
from unittest.mock import Mock
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.unit.data import Data
from src.groups.base.container import BaseContainer


class TestData(unittest.TestCase):
    def setUp(self):
        self.container_mock = Mock(spec=BaseContainer)

    def test_data_creation(self):
        data = Data(self.container_mock)
        self.assertEqual(data.data, self.container_mock)
