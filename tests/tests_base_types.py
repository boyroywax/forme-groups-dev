import unittest
import sys
import random

from typing import Union, TypeAlias, Any, Optional, TypeVar, Type, Tuple, Callable, Iterable, Iterator, Sequence, Mapping, MutableMapping, Set, MutableSet, MappingView, KeysView, ItemsView, ValuesView, Awaitable, AsyncIterable, AsyncIterator, Coroutine, Collection, Container, Reversible, Generator, AsyncGenerator, SupportsAbs, SupportsBytes, SupportsComplex, SupportsFloat, SupportsIndex, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.types import BaseValueTypes, BaseTypesInterface


class TestBaseTypesInterface(unittest.TestCase):
    def setUp(self):
        class base_types_interface(BaseTypesInterface):
            Int = int
            Float = float
            Bool = bool
            Str = str
            Bytes = bytes

            @property
            def all(self) -> Union[TypeAlias, TypeAlias]:
                return int | float | bool | str | bytes

            @property
            def aliases(self) -> dict[TypeAlias, tuple[str]]:
                return {
                    self.Int: ("int", "integer"),
                    self.Float: ("float", "floating_point"),
                    self.Bool: ("bool", "boolean"),
                    self.Str: ("str", "string"),
                    self.Bytes: ("bytes", "bytestring")
                }

        self.base_types_interface = base_types_interface()

    def test_base_type_interface_init_(self):
        self.assertEqual(
            self.base_types_interface.aliases, {
                self.base_types_interface.Int: ("int", "integer"),
                self.base_types_interface.Float: ("float", "floating_point"),
                self.base_types_interface.Bool: ("bool", "boolean"),
                self.base_types_interface.Str: ("str", "string"),
                self.base_types_interface.Bytes: ("bytes", "bytestring")
            }
        )

    def test_base_type_interface_has_slots(self):
        for slot in self.base_types_interface.__slots__:
            self.assertEqual(hasattr(self.base_types_interface, slot), True)

    def test_base_type_interface_has_no_weakref_slot(self):
        self.assertFalse(hasattr(self.base_types_interface, "__weakref__"))

    def test_base_type_interface_has_no_dict(self):
        self.assertEqual(hasattr(self.base_types_interface, "__dict__"), False)

    def test_base_type_interface_str(self):
        self.assertEqual(str(self.base_types_interface), " ")

    




class TestBaseTypes(unittest.TestCase):
    def setUp(self):
        self.base_value_types = BaseValueTypes()

    def test_init_with_str(self):
        self.assertEqual(self.base_value_types.Integer, int)
        self.assertEqual(self.base_value_types.FloatingPoint, float)
        self.assertEqual(self.base_value_types.Boolean, bool)
        self.assertEqual(self.base_value_types.String, str)
        self.assertEqual(self.base_value_types.Bytes, bytes)
        self.assertEqual(self.base_value_types.Number, int | float)
        self.assertEqual(self.base_value_types.Text, str | bytes | bool | None)

    def test_base_value_type_has_slots(self):
        for slot in self.base_value_types.__slots__:
            self.assertTrue(hasattr(self.base_value_types, slot))

    def test_base_value_type_has_no_weakref_slot(self):
        self.assertFalse(hasattr(self.base_value_types, "__weakref__"))

    def test_base_value_type_has_no_dict(self):
        self.assertFalse(hasattr(self.base_value_types, "__dict__"))

    def test_base_value_type_str(self):
        self.assertEqual(str(self.base_value_types), " ")



        
