import unittest
from unittest.mock import Mock
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.unit.owner import Owner
from src.groups.base.container import BaseContainer


class TestOwner(unittest.TestCase):
    def setUp(self):
        self.container_mock = Mock(spec=BaseContainer)

    def test_owner_creation(self):
        owner = Owner(self.container_mock)
        self.assertEqual(owner.owner, self.container_mock)