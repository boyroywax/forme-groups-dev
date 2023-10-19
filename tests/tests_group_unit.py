import unittest
import sys
import random
import uuid

sys.path.append("../forme-groups-python-3-12/")

from src.groups.unit import GroupUnit
from src.groups.unit.nonce import Nonce
from src.groups.unit.data import Data
from src.groups.unit.credential import Credential
from src.groups.unit.owner import Owner
from src.groups.base.container import BaseContainer
from src.groups.base.value import BaseValue
from src.groups.base.schema import BaseSchema, SchemaEntry


__RANGE__ = 1000


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

        self.assertEqual(repr(self.group_unit.owner), "Owner(_owner=None)")
        self.assertEqual(str(self.group_unit.owner), "")

        self.assertEqual(repr(self.group_unit.credential), "Credential(_credential=None)")
        self.assertEqual(str(self.group_unit.credential), "")

        self.assertEqual(repr(self.group_unit.data), "Data(_entry=BaseContainer(items=(BaseValue(value=1, type=int),), type=tuple), _schema=BaseSchema(entries=(SchemaEntry(key='test', value=int),)))")

    def test_init_with_data(self):
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(self.group_unit.data, self.data)

    def test_create_random_group_units(self):
        group_units = []
        group_unit_hashses = []
        groups_units_hashed = ()
        for i in range(__RANGE__):
            values = [
                random.randint(0, 10000000000),
                random.randbytes(256),
                random.choice([True, False]),
                random.random(),
                None,
                str(uuid.uuid4())
            ]
            random_value = random.choice(values)
            value = BaseValue(random_value)
            value2 = BaseValue(random_value)
            base_container = BaseContainer((value, value2), "tuple")
            data = Data(base_container)
            nonce = Nonce._next_active_nonce(Nonce(BaseContainer((0 + i, ), "tuple")))
            # print(f'nonce: {nonce}')
            credential = Credential()
            owner = Owner()
            group_units.append(GroupUnit(nonce, owner, credential, data))
            # group_unit_hashses.append(group_units[i]._hash_package().root())
            # group_units_hahsed += ((group_units[i]._hash_package().root(), group_units[i]), )

        self.assertEqual(len(group_units), __RANGE__)
