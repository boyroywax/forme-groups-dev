import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")

from src.groups.utils.checks import (
    is_base_container_type,
    is_base_value_type,
    is_linear_container,
    is_named_container,
    _contains_sub_container
)


class TestChecks(unittest.TestCase):
    def test_is_base_value_type(self):
        self.assertTrue(is_base_value_type("BaseValue"))

    def test_is_base_value_type_false(self):
        self.assertFalse(is_base_value_type([]))
        self.assertFalse(is_base_value_type(()))
        self.assertFalse(is_base_value_type({}))
        self.assertFalse(is_base_value_type(set()))
        self.assertFalse(is_base_value_type(frozenset()))

    def test_is_base_value_type_true(self):
        self.assertTrue(is_base_value_type(1))
        self.assertTrue(is_base_value_type(1.0))
        self.assertTrue(is_base_value_type(True))
        self.assertTrue(is_base_value_type(False))
        self.assertTrue(is_base_value_type(""))

    def test_is_base_container_type(self):
        self.assertFalse(is_base_container_type("BaseContainer"))

    def test_is_base_container_type_false(self):
        self.assertFalse(is_base_container_type(1))
        self.assertFalse(is_base_container_type(1.0))
        self.assertFalse(is_base_container_type(True))
        self.assertFalse(is_base_container_type(False))
        self.assertFalse(is_base_container_type(""))

    def test_is_base_container_type_true(self):
        self.assertTrue(is_base_container_type([]))
        self.assertTrue(is_base_container_type(()))
        self.assertTrue(is_base_container_type({}))
        self.assertTrue(is_base_container_type(set()))
        self.assertTrue(is_base_container_type(frozenset()))

    def test_is_linear_container(self):
        self.assertTrue(is_linear_container(["str", "str", "str"]))


    def test_is_linear_container_false(self):
        self.assertFalse(is_linear_container({}))
        self.assertFalse(is_linear_container(1))
        self.assertFalse(is_linear_container(1.0))
        self.assertFalse(is_linear_container(True))
        self.assertFalse(is_linear_container(False))
        self.assertFalse(is_linear_container(""))

    def test_is_linear_container_true(self):
        self.assertTrue(is_linear_container([]))
        self.assertTrue(is_linear_container(()))
        self.assertTrue(is_linear_container(set()))
        self.assertTrue(is_linear_container(frozenset()))

    def test_is_named_container(self):
        self.assertTrue(is_named_container({"key": "value"}))

    def test_is_named_container_false(self):
        self.assertFalse(is_named_container([]))
        self.assertFalse(is_named_container(()))
        self.assertFalse(is_named_container(set()))
        self.assertFalse(is_named_container(frozenset()))
        self.assertFalse(is_named_container(1))
        self.assertFalse(is_named_container(1.0))
        self.assertFalse(is_named_container(True))
        self.assertFalse(is_named_container(False))
        self.assertFalse(is_named_container(""))

    def test_is_named_container_true(self):
        self.assertTrue(is_named_container({}))

    def test_contains_sub_container(self):
        self.assertTrue(_contains_sub_container({"key": ["value", "value2"]}))

    def test_contains_sub_container_false(self):
        self.assertFalse(_contains_sub_container([]))
        self.assertFalse(_contains_sub_container(()))
        self.assertFalse(_contains_sub_container(set()))
        self.assertFalse(_contains_sub_container(frozenset()))
        self.assertFalse(_contains_sub_container(1))
        self.assertFalse(_contains_sub_container(1.0))
        self.assertFalse(_contains_sub_container(True))
        self.assertFalse(_contains_sub_container(False))
        self.assertFalse(_contains_sub_container(""))
        self.assertFalse(_contains_sub_container({"key": "value"}))

    def test_contains_sub_container_true(self):
        self.assertTrue(_contains_sub_container({"key": {"key": "value"}}))
        self.assertTrue(_contains_sub_container({"key": {"key": {"key": "value"}}}))
        self.assertTrue(_contains_sub_container({"key": {"key": {"key": {"key": "value"}}}}))
        self.assertTrue(_contains_sub_container({"key": {"key": {"key": {"key": {"key": "value"}}}}}))
        self.assertTrue(_contains_sub_container({"key": {"key": {"key": {"key": {"key": {"key": "value"}}}}}}))
        self.assertTrue(_contains_sub_container({"key": {"key": {"key": {"key": {"key": {"key": {"key": "value"}}}}}}}))
        self.assertTrue(_contains_sub_container({"key": {"key": {"key": {"key": {"key": {"key": {"key": {"key": "value"}}}}}}}}))
        self.assertTrue(_contains_sub_container({"key": {"key": {"key": {"key": {"key": {"key": {"key": {"key": {"key": "value"}}}}}}}}}))

