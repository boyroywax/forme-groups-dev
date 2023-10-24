import unittest
from unittest.mock import Mock
import sys
from src.groups.base.value import BaseValue

sys.path.append("../forme-groups-python-3-12/")
from src.groups.unit.data import Data
from src.groups.base.container import BaseContainer
from src.groups.base.schema import BaseSchema, SchemaEntry


class TestData(unittest.TestCase):
    def setUp(self):
        self.container_mock = Mock(spec=BaseContainer)
        self.schema_mock = Mock(spec=BaseSchema)
        self.schema_real = BaseSchema((SchemaEntry("name", "string"), SchemaEntry("age", "integer")))
        self.data_real = Data(BaseContainer((BaseValue("test_user"), BaseValue(31)), "tuple"))
        self.data_bad = Data(BaseContainer((BaseValue(b'ccc'), BaseValue(31)), "tuple"))

    def test_data_creation(self):
        data = Data(self.container_mock)
        self.assertEqual(data.data, self.container_mock)

    def test_data_creation_with_schema(self):
        data = Data(self.container_mock, self.schema_mock)
        self.assertEqual(data.data, self.container_mock)
        self.assertEqual(data.schema, self.schema_mock)

    def test_data_creation_with_schema_real(self):
        produced_data = Data._from(self.data_real.data, self.schema_real)
        print(produced_data)
        self.assertEqual(produced_data.data, self.data_real.data)
    
    def test_data_creation_with_schema_real_bad(self):
        self.assertRaises(TypeError, Data._from, self.data_bad.data, self.schema_real)
