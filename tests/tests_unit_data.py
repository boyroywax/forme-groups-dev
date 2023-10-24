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
        self.schema_real = BaseSchema((SchemaEntry("name", "string"), SchemaEntry("age", "integer")))
        self.data_real = Data(BaseContainer((BaseValue("test_user"), BaseValue(31)), "tuple"))
        self.data_bad = Data(BaseContainer((BaseValue(b'ccc'), BaseValue(31)), "tuple"))

    def test_data_creation_with_schema_real(self):
        produced_data = Data._from(self.data_real.entry, self.schema_real)
        print(produced_data)
        self.assertEqual(produced_data.entry, self.data_real.entry)
    
    def test_data_creation_with_schema_real_bad(self):
        self.assertRaises(TypeError, Data._from, self.data_bad.entry, None, self.schema_real)

    def test_data_creation_with_no_schema(self):
        data_no_schema = Data(self. data_real.entry)
        self.assertEqual(data_no_schema.entry, self.data_real.entry)

    def test_data_creation_str(self):
        self.assertEqual(str(self.data_real), f"entry: ('test_user', 31), schema: None")