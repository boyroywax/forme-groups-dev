import unittest
import sys
import random

from attrs import define


sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.interface import BaseInterface


class TestBaseInterface(unittest.TestCase):
    def setUp(self):

        @define(frozen=True, slots=True, weakref_slot=False)
        class base_interface(BaseInterface):
            test_property: int = 1
            _private_test_property: int = 2

        self.base_interface = base_interface()
        

        @define(frozen=True, slots=True, weakref_slot=False)
        class BaseInterfaceExample(BaseInterface):
            test_property: int = 1
            test_string: str = "test"
            test_bool: bool = True
            test_float: float = 1.0
            test_bytes: bytes = b"test"
            test_none: None = None
            _private_test_property: int = 2

        self.base_interface2 = BaseInterfaceExample()

    def test_base_interface_init_(self):
        self.assertEqual(self.base_interface.__slots__, ("test_property", "_private_test_property"))

    def test_base_interface_has_slots(self):
        self.assertEqual(len(self.base_interface.__slots__), 2)

    def test_base_interface_has_no_weakref_slot(self):
        self.assertFalse(hasattr(self.base_interface, "__weakref__"))

    def test_base_interface_has_no_dict(self):
        self.assertEqual(hasattr(self.base_interface, "__dict__"), False)

    def test_base_interface_str(self):
        self.assertEqual(str(self.base_interface), "test_property: 1")

    def test_base_interface_repr(self):
        self.assertEqual(repr(self.base_interface), "base_interface(test_property=1, _private_test_property=2)")

    def test_base_interface_hash_leaf(self):
        self.assertEqual(self.base_interface._hash_leaf(), "d9e12b2e12010e3b8cd2022e84400d1eb68a4f377069d8759888f6e96082f1e9")

    def test_base_interface_iter(self):
        self.assertEqual(list(self.base_interface), ["test_property", "_private_test_property"])
        self.assertEqual(getattr(self.base_interface, "test_property"), 1)
        self.assertEqual(getattr(self.base_interface, "_private_test_property"), 2)

    def test_base_interface_is_frozen(self):
        with self.assertRaises(AttributeError):
            self.base_interface.test_property = 2

    def test_base_interface_more_properties(self):

        self.assertEqual(self.base_interface2._hash_leaf(), "b4c5b6872918d107cff29a9b6a0c81e7c2c450dd46285055beb0deefefa04271")

        self.assertEqual(str(self.base_interface2), "test_property: 1, test_string: test, test_bool: True, test_float: 1.0, test_bytes: b'test', test_none: None")
        self.assertEqual(repr(self.base_interface2), "BaseInterfaceExample(test_property=1, test_string='test', test_bool=True, test_float=1.0, test_bytes=b'test', test_none=None, _private_test_property=2)")

    def test_base_interface2_is_frozen(self):
        with self.assertRaises(AttributeError):
            self.base_interface2.test_property = 2

    def test_base_interface_only_private_str(self):
        self.assertEqual(self.base_interface.__str_private__(include_underscored_slots=True, private_only=True), "_private_test_property: 2")

    def test_base_interface_only_private_repr(self):
        self.assertEqual(self.base_interface.__repr_private__(include_underscored_slots=True, private_only=True), "base_interface(_private_test_property=2)")