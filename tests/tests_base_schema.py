import unittest
import sys

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from src.groups.base.schema import BaseSchema, SchemaEntry


class TestBaseSchema(unittest.TestCase):
    def setUp(self):
        self.schema_entry_one = SchemaEntry("name", "string")
        self.schema_entry_two = SchemaEntry("age", "number")

        self.base_schema_one = BaseSchema((self.schema_entry_one, self.schema_entry_two, ))

    def test_init_with_schema_entry(self):
        self.assertEqual(self.base_schema_one._schema, (self.schema_entry_one, self.schema_entry_two))