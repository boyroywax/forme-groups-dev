import sys
import unittest

sys.path.append("../forme-groups-python-3-12/")
from src.groups.utils.converters import convert_to_bytes


class TestConverters(unittest.TestCase):
    def test_convert_to_bytes(self):
        value = 1
        self.assertEqual(convert_to_bytes(value), b'\x01')

    def test_convert_to_bytes_bad_types(self):
        value = {"test": 1}
        self.assertRaises(TypeError, convert_to_bytes, value)

    def test_convert_to_bytes_bad_types_two(self):
        value = ["test", 1]
        self.assertRaises(TypeError, convert_to_bytes, value)
