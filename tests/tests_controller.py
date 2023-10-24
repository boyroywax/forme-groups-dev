import unittest
from unittest.mock import Mock
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.base.value import BaseValue
from src.groups.base.container import BaseContainer
from src.groups.base.schema import BaseSchema, SchemaEntry
from src.groups.unit.nonce import Nonce
from src.groups.unit.data import Data
from src.groups.controller import Controller


class TestController(unittest.TestCase):
    def setUp(self):
        self.schema_real = BaseSchema((SchemaEntry("name", "string"), SchemaEntry("age", "integer")))
        self.data_real = Data(BaseContainer((BaseValue("test_user"), BaseValue(31)), "tuple"))
        self.data_bad = Data(BaseContainer((BaseValue(b'ccc'), BaseValue(31)), "tuple"))
        self.defualt_nonce = Nonce(BaseContainer((BaseValue(1), ), "tuple"))
        self.controller = Controller()
        self.controller._create_group_unit(self.data_real)

    def test_controller_add_data(self):
        self.assertEqual(self.controller.active.data.entry, self.data_real.entry )

    def test_controller_add_data_bad(self):
        self.controller._create_group_unit(self.data_bad)
        self.assertEqual(self.controller.active.data.entry, self.data_bad.entry)

    def test_controller_add_data_bad_with_schema(self):
        self.assertRaises(AttributeError, self.controller._create_group_unit, self.data_bad, None, self.schema_real)

    def test_controller_add_data_with_schema(self):
        self.controller._create_group_unit(self.data_real, self.schema_real)
        self.assertEqual(self.controller.active.data.entry, self.data_real.entry)

    def test_controller_add_data_nonce(self):
        self.assertEqual(self.controller.active.nonce._hash().root(), '3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd')
        self.assertEqual(self.controller.active.nonce, self.defualt_nonce)