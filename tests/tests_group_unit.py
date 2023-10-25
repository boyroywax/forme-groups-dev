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
        self.credential = Credential(self.base_container)
        self.owner = Owner(self.base_container)

    def test_init(self):
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(repr(self.group_unit.nonce), "Nonce(chain=BaseContainer(items=(BaseValue(value=0, type=int),), type=tuple))")
        self.assertEqual(str(self.group_unit.nonce), "0")

        self.assertEqual(repr(self.group_unit.owner), "Owner(_owner=BaseContainer(items=(BaseValue(value=1, type=int),), type=tuple))")
        self.assertEqual(str(self.group_unit.owner), "")

        self.assertEqual(repr(self.group_unit.credential), "Credential(_credential=BaseContainer(items=(BaseValue(value=1, type=int),), type=tuple))")
        self.assertEqual(str(self.group_unit.credential), "")

        self.assertEqual(repr(self.group_unit.data), "Data(entry=BaseContainer(items=(BaseValue(value=1, type=int),), type=tuple), schema=BaseSchema(entries=(SchemaEntry(key='test', value=int),)))")

    def test_init_with_data(self):
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(self.group_unit.data, self.data)

    def test_create_random_group_units(self):
        group_units = []
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

        self.assertEqual(len(group_units), __RANGE__)

    
    def test_to_dict(self):
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(self.group_unit.to_dict(), {
            "nonce": self.group_unit.nonce._to_dict(),
            "owner": self.group_unit.owner._to_dict(),
            "credential": self.group_unit.credential._to_dict(),
            "data": self.group_unit.data._to_dict()
        })

    def test_from_dict(self):
        group_unit_dict: dict = {
            "nonce": self.nonce._to_dict(),
            "owner": self.owner._to_dict(),
            "credential": self.credential._to_dict(),
            "data": self.data._to_dict()
        }
        print(group_unit_dict)
        group_unit = GroupUnit.from_dict(group_unit_dict)
        self.assertEqual(group_unit, GroupUnit.from_dict(group_unit.to_dict()))

    def test_print(self):
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(str(self.group_unit._print()), "Group Unit:\nNonce: 0\nOwner: (1,)\nCredential: (1,)\nData: {'items': [{'value': 1, 'type': 'int'}], 'type': 'tuple'}")

    def test_to_json(self):
        self.maxDiff = None
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)
        self.assertEqual(self.group_unit.to_json(), '{"nonce": {"chain": {"items": [{"value": 0, "type": "int"}], "type": "tuple"}}, "owner": {"owner": {"items": [{"value": 1, "type": "int"}], "type": "tuple"}}, "credential": {"credential": {"items": [{"value": 1, "type": "int"}], "type": "tuple"}}, "data": {"entry": {"items": [{"value": 1, "type": "int"}], "type": "tuple"}, "schema": {"entries": [{"key": "test", "value": "int"}]}}}')