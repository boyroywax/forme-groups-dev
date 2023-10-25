import unittest
import sys
import json

sys.path.append("../forme-groups-python-3-12/")
from src.groups.unit.credential import Credential
from src.groups.unit.owner import Owner
from src.groups.base.container import BaseContainer
from src.groups.unit.nonce import Nonce
from src.groups.unit.data import Data
from src.groups import Groups
from src.groups.unit import GroupUnit


class TestGroups(unittest.TestCase):
    def setUp(self):
        self.container_mock = BaseContainer((1, 2, 3))
        self.owner = Owner(self.container_mock)
        self.credentials = Credential(self.container_mock)
        self.data = Data(self.container_mock)
        self.nonce = Nonce(BaseContainer((0, )))
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credentials, self.data)
        # with open('state-test.json', 'w') as f:
        #     f.write(json.dumps(self.group_unit.to_dict()))

    def test_groups_creation_init(self):
        self.groups = Groups(state_file='state-test.json')
        print(self.groups.controller.active)

    def test_groups_creation(self):
        self.assertEqual(self.groups.controller.pool.group_units[-1][2].owner, self.owner)

    def test_groups_has_slots(self):
        self.assertEqual(self.groups.__slots__, ('controller', 'state_file'))
