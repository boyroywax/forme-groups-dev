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

    def test_owner_has_slots(self):
        owner = Owner(self.container_mock)
        self.assertEqual(owner.__slots__, ('_owner', ))

    def test_owner_hash_slots_non_mock(self):
        owner = Owner(BaseContainer((1, 2, 3)))
        self.assertEqual(owner.__slots__, ('_owner', ))

    def test_owner_to_dict_non_mock(self):
        owner = Owner(BaseContainer((1, 2, 3)))
        self.assertEqual(owner._to_dict(), {'owner': {'items': [{'value': 1, 'type': 'int'}, {'value': 2, 'type': 'int'}, {'value': 3, 'type': 'int'}], 'type': 'tuple'}})