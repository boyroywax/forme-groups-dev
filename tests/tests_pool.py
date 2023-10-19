import unittest
import sys
import random
import uuid

sys.path.append("../forme-groups-python-3-12/")
from src.groups.base.value import BaseValue
from src.groups.base.container import BaseContainer
from src.groups.pool import Pool
from src.groups.unit import GroupUnit
from src.groups.unit.data import Data
from src.groups.unit.credential import Credential
from src.groups.unit.owner import Owner
from src.groups.unit.nonce import Nonce


__RANGE__ = 1000


class TestPool(unittest.TestCase):
    def setUp(self):
        self.data = Data(BaseContainer((BaseValue(1), ), "tuple"))
        self.credential = Credential()
        self.owner = Owner()
        self.nonce = Nonce()
        self.group_unit = GroupUnit(self.nonce, self.owner, self.credential, self.data)

    def test_init(self):
        self.pool = Pool(((self.group_unit._hash_package().root(), self.group_unit), ))
        self.assertEqual(self.pool.group_units, ((self.group_unit._hash_package().root(), self.group_unit), ))

    def test_init_with_bad_type(self):
        self.assertRaises(TypeError, Pool, (self.group_unit, ))

    def test_pool_check_if_exists(self):
        self.pool = Pool(((self.group_unit._hash_package().root(), self.group_unit), ))
        self.assertTrue(self.pool.check_if_exists(self.group_unit))

    def test_create_random_group_units(self):
        group_units = []
        group_unit_hashses = []
        group_units_hashed = ()
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
            group_units_hashed += ((group_units[i]._hash_package().root(), group_units[i]), )

        self.assertEqual(len(group_units), __RANGE__)

        pool = Pool(group_units_hashed)

        for item in group_units_hashed:
            self.assertTrue(pool.check_if_exists(item[1]))

    def test_group_unit_add_group_unit(self):
        self.pool = Pool()
        self.pool.add_group_unit(self.group_unit)
        self.assertEqual(self.pool.group_units, ((self.group_unit._hash_package().root(), self.group_unit), ))

        self.assertRaises(TypeError, self.pool.add_group_unit, (self.group_unit._hash_package().root(), self.group_unit))