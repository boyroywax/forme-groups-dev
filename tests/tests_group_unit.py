import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")

from src.groups.unit import GroupUnit
from src.groups.unit.nonce import Nonce
from src.groups.unit.data import Data
from src.groups.unit.credential import Credential
from src.groups.unit.owner import Owner
from src.groups.base.container import BaseContainer
from src.groups.base.value import BaseValue
from src.groups.base.schema import BaseSchema, SchemaEntry


class TestGroupUnit(unittest.TestCase):
    def setUp(self):
        self.schema_entry = SchemaEntry("test", "int")
        self.schema = BaseSchema((self.schema_entry, ))
        self.base_container = BaseContainer((BaseValue(1), ), "tuple")
        self.data = Data(self.base_container, self.schema)
        self.nonce = Nonce()
        self.credential = Credential()
        self.owner = Owner()

    def test_init(self):
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(repr(self.group_unit.nonce), "Nonce(chain=BaseContainer(items=(BaseValue(value=0, type=int),), type=tuple))")
        self.assertEqual(str(self.group_unit.nonce), "0")

    def test_init_with_data(self):
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(self.group_unit.data, self.data)


