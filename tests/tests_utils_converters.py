import sys
import unittest

sys.path.append("../forme-groups-python-3-12/")
from src.groups.utils.converters import (
    convert_to_bytes,
    convert_to_int,
    convert_to_str,
    convert_to_bool,
    convert_to_float,
    force_value_type,
    convert_tuple)
from src.groups.base.value import BaseValue

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
        self.assertEqual(force_value_type(value, "int"), 1)
        self.assertEqual(force_value_type(value, "str"), "1")
        self.assertEqual(force_value_type(value, "bytes"), b'\x01')
        self.assertEqual(force_value_type(value, "bool"), True)
        self.assertEqual(force_value_type(value, "float"), 1.0)

    def test_force_value_types_bad_types(self):
        value = {"test": 1}
        self.assertRaises(AssertionError, force_value_type, value, "int")
        self.assertRaises(AssertionError, force_value_type, value, "str")
        self.assertRaises(AssertionError, force_value_type, value, "bytes")
        self.assertRaises(AssertionError, force_value_type, value, "bool")
        self.assertRaises(AssertionError, force_value_type, value, "float")
    

    def test_convert_tuple(self):
        value = (1, 2, 3)
        self.assertEqual(convert_tuple(value, type_alias="tuple"), (1, 2, 3))






