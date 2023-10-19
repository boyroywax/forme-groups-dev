import sys
import unittest

sys.path.append("../forme-groups-python-3-12/")
from src.groups.utils.converters import convert_to_bytes, convert_to_int, convert_to_str, convert_to_bool, convert_to_float, force_value_type


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

    def test_convert_to_int(self):
        value: bytes = b'\x01'
        self.assertEqual(convert_to_int(value), 1)

    def test_convert_to_int_bad_types(self):
        value: dict = {"test": 1}
        self.assertRaises(TypeError, convert_to_int, value)

    def test_convert_to_int_bad_types_two(self):
        value: list = ["test", 1]
        self.assertRaises(TypeError, convert_to_int, value)

    def test_convert_to_str(self):
        value: bytes = b'\x01'
        self.assertEqual(convert_to_str(value), '1')

    def test_convert_to_str_bad_types(self):
        value = {"test": 1}
        self.assertRaises(TypeError, convert_to_str, value)

    def test_convert_to_str_bad_types_two(self):
        value = ["test", 1]
        self.assertRaises(TypeError, convert_to_str, value)

    def test_convert_to_bool(self):
        value: bytes = b'\x01'
        self.assertEqual(convert_to_bool(value), True)

    def test_convert_to_bool_bad_types(self):
        value = {"test": 1}
        self.assertRaises(TypeError, convert_to_bool, value)

    def test_convert_to_bool_bad_types_two(self):
        value = ["test", 1]
        self.assertRaises(TypeError, convert_to_bool, value)

    def test_convert_to_float(self):
        value: bytes = b'\x00\x00\x80\x3f'
        self.assertEqual(convert_to_float(value), 1.0)

    def test_convert_to_float_bad_types(self):
        value = {"test": 1}
        self.assertRaises(TypeError, convert_to_float, value)

    def test_convert_to_float_bad_types_two(self):
        value = ["test", 1]
        self.assertRaises(TypeError, convert_to_float, value)

    def test_force_value_type(self):
        value = 1
        self.assertEqual(force_value_type(value, "int"), 1)

    def test_force_value_type_bad_types(self):
        value = {"test": 1}
        self.assertRaises(AssertionError, force_value_type, value, "int")

    def test_force_value_type_bad_types_two(self):
        value = ["test", 1]
        self.assertRaises(AssertionError, force_value_type, value, "int")

    def test_force_value_types(self):
        value = 1
        self.assertEqual(force_value_type(value, "<class 'int'>"), 1)

        value = "1"
        self.assertEqual(force_value_type(value, "<class 'int'>"), 1)

        value = 1.0
        self.assertEqual(force_value_type(value, "<class 'int'>"), 1)

        value = True
        self.assertEqual(force_value_type(value, "<class 'int'>"), 1)

        value = False
        self.assertEqual(force_value_type(value, "<class 'int'>"), 0)

        value = b'\x01'
        self.assertEqual(force_value_type(value, "<class 'int'>"), 1)







