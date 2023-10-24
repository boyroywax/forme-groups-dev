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
        self.container_mock = Mock(spec=BaseContainer)
        self.schema_mock = Mock(spec=BaseSchema)
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

    def test_controller_add_data_bad_two(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock)

    def test_controller_add_data_bad_three(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.schema_mock)

    def test_controller_add_data_bad_four(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.schema_real)

    def test_controller_add_data_bad_five(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.data_real, self.schema_real)

    def test_controller_add_data_bad_six(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.data_bad, self.schema_real)

    def test_controller_add_data_bad_seven(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock, self.schema_real)

    def test_controller_add_data_bad_eight(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock, self.data_real)

    def test_controller_add_data_bad_nine(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock, self.schema_mock)

    def test_controller_add_data_bad_ten(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock, self.schema_real, self.data_real)

    def test_controller_add_data_bad_eleven(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock, self.schema_real, self.data_bad)

    def test_controller_add_data_bad_twelve(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock, self.schema_mock, self.data_real)

    def test_controller_add_data_bad_thirteen(self):
        self.assertRaises(TypeError, self.controller._create_group_unit, self.container_mock, self.schema_mock, self.data_bad)