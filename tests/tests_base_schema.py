import unittest
import sys

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from src.groups.base.schema import BaseSchema, SchemaEntry
from src.groups.base.container import BaseContainer


class TestBaseSchema(unittest.TestCase):
    def setUp(self):
        self.schema_entry_one = SchemaEntry("name", "string")
        self.schema_entry_two = SchemaEntry("age", "integer")
        self.schema_base_one = BaseSchema((self.schema_entry_one, self.schema_entry_two))

    def test_init_with_schema_entry(self):
        self.assertEqual(self.schema_base_one._entries, (self.schema_entry_one, self.schema_entry_two))

    def test_inint_with_improper_schema_entries(self):
        self.assertRaises(TypeError, BaseSchema, (self.schema_entry_one, "string"))

    def test_init_with_improper_schema_entry(self):
        self.assertRaises(AssertionError, SchemaEntry, "name", "bad_type")