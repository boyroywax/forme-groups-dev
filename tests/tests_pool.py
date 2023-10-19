import unittest
import sys
from unittest.mock import MagicMock

sys.path.append("../forme-groups-python-3-12/")
from src.groups.base.value import BaseValue
from src.groups.base.container import BaseContainer
from src.groups.pool import Pool
from src.groups.unit import GroupUnit
from src.groups.unit.data import Data
from src.groups.unit.credential import Credential
from src.groups.unit.owner import Owner
from src.groups.unit.nonce import Nonce


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
            