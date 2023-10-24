import unittest
from unittest.mock import Mock
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.base.value import BaseValue
from src.groups.base.container import BaseContainer
from src.groups.base.schema import BaseSchema, SchemaEntry
from src.groups.unit.data import Data
from src.groups.controller import Controller


class TestController(unittest.TestCase):
    def setUp(self):
        self.schema_real = BaseSchema((SchemaEntry("name", "string"), SchemaEntry("age", "integer")))
        self.data_real = Data(BaseContainer((BaseValue("test_user"), BaseValue(31)), "tuple"))
        self.data_bad = Data(BaseContainer((BaseValue(b'ccc'), BaseValue(31)), "tuple"))
        self.controller = Controller()
        self.controller._create_group_unit(self.data_real)

    def test_controller_add_data(self):
        self.assertEqual(self.controller.active.data.entry, self.data_real.entry )

    def test_controller_add_data_bad(self):
        self.controller._create_group_unit(self.data_bad)
        self.assertEqual(self.controller.active.data.entry, self.data_bad.entry)

