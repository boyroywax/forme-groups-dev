import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")

from src.groups.unit import GroupUnit
from src.groups.unit.exceptions import GroupUnitException


class TestGroupUnit(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        self.assertRaises(GroupUnitException, GroupUnit, "test")

