import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.base.schema import BaseSchema, SchemaEntry
from src.groups.base.container import BaseContainer
from src.groups.base.exceptions import GroupBaseTypeException


class TestBaseSchema(unittest.TestCase):
    def setUp(self):
        self.schema_entry_one = SchemaEntry("name", "string")
        self.schema_entry_two = SchemaEntry("age", "integer")
        self.schema_base_one = BaseSchema((self.schema_entry_one, self.schema_entry_two))

    def test_schema_entry_hash(self):
        self.assertEqual(self.schema_entry_one._hash().root(), 'fbc595a11273e6f79f13f9210d7d60660c8ad127aa6b870b841c4b2a8ff75cb2')

    def test_schema_entry_repr(self):
        self.assertEqual(repr(self.schema_entry_one), "SchemaEntry(key='name', value=str)")

    def test_schema_entry_str(self):
        self.assertEqual(str(self.schema_entry_one), "key=name, value=str")

    def test_schema_entry_has_slots(self):
        self.assertEqual(self.schema_entry_one.__slots__, ('_key', '_value'))

    def test_schema_entry_key(self):
        self.assertEqual(self.schema_entry_one._key, "name")

    def test_schema_entry_value(self):
        self.assertEqual(self.schema_entry_one._value, str)

    def test_schema_entry_hash_key(self):
        self.assertEqual(self.schema_entry_one._hash_key(), '82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89')

    def test_schema_entry_hash_value(self):
        self.assertEqual(self.schema_entry_one._hash_value(), '8c25cb3686462e9a86d2883c5688a22fe738b0bbc85f458d2d2b5f3f667c6d5a')

    def test_schema_entry_hash_repr(self):
        self.assertEqual(repr(self.schema_entry_one._hash()), "MerkleTree(root=fbc595a11273e6f79f13f9210d7d60660c8ad127aa6b870b841c4b2a8ff75cb2)")

    def test_schema_entry_hash_two(self):
        self.assertEqual(self.schema_entry_two._hash().root(), '5422c43fc239d7228d8aca8f9310bca3ce00cea3256adb0db595a2b1c211a7e4')

    def test_init_with_schema_entry(self):
        self.assertEqual(self.schema_base_one._entries, (self.schema_entry_one, self.schema_entry_two))

    def test_inint_with_improper_schema_entries(self):
        self.assertRaises(TypeError, BaseSchema, (self.schema_entry_one, "string"))

    def test_init_with_improper_schema_entry(self):
        self.assertRaises(GroupBaseTypeException, SchemaEntry, "name", "bad_type")