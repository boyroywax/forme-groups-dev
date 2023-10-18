import unittest
import sys
import random
from attrs import define

from typing import Union, TypeAlias, Any, Optional, TypeVar, Type, Tuple, Callable, Iterable, Iterator, Sequence, Mapping, MutableMapping, Set, MutableSet, MappingView, KeysView, ItemsView, ValuesView, Awaitable, AsyncIterable, AsyncIterator, Coroutine, Collection, Container, Reversible, Generator, AsyncGenerator, SupportsAbs, SupportsBytes, SupportsComplex, SupportsFloat, SupportsIndex, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString, SupportsRound, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsAbs, SupportsIndex, SupportsBytes, SupportsComplex, SupportsFloat, SupportsInt, SupportsRound, ByteString

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from src.groups.base.types import BaseTypes
from src.groups.base.exceptions import GroupBaseTypeException

class TestBaseTypes(unittest.TestCase):
#     def setUp(self):

#         @define(frozen=True, slots=True, weakref_slot=False)
#         class BaseTypesExample(BaseTypesInterface):
#             integer: TypeAlias = int
#             floating_point: TypeAlias = float
#             boolean: TypeAlias = bool
#             string: TypeAlias = str
#             bytes_: TypeAlias = bytes

#             @property
#             def all(self) -> Union[TypeAlias, TypeAlias]:
#                 return int | float | bool | str | bytes

#             @property
#             def aliases(self) -> dict[TypeAlias, tuple[str]]:
#                 return {
#                     self.integer: ("int", "integer"),
#                     self.floating_point: ("float", "floating_point"),
#                     self.boolean: ("bool", "boolean"),
#                     self.string: ("str", "string"),
#                     self.bytes_: ("bytes", "bytestring")
#                 }

#         self.base_types_interface = BaseTypesExample()

#     def test_base_type_interface_init_(self):
#         self.assertEqual(
#             self.base_types_interface.aliases, {
#                 self.base_types_interface.integer: ("int", "integer"),
#                 self.base_types_interface.floating_point: ("float", "floating_point"),
#                 self.base_types_interface.boolean: ("bool", "boolean"),
#                 self.base_types_interface.string: ("str", "string"),
#                 self.base_types_interface.bytes_: ("bytes", "bytestring")
#             }
#         )

#     def test_base_type_interface_has_slots(self):
#         for slot in self.base_types_interface.__slots__:
#             self.assertEqual(hasattr(self.base_types_interface, slot), True)

#     def test_base_type_interface_has_no_weakref_slot(self):
#         self.assertFalse(hasattr(self.base_types_interface, "__weakref__"))

#     def test_base_type_interface_has_no_dict(self):
#         self.assertEqual(hasattr(self.base_types_interface, "__dict__"), False)

#     def test_base_type_interface_repr(self):
#         print(self.base_types_interface.__slots__)
#         self.assertEqual(repr(self.base_types_interface), "BaseTypesExample(integer=<class 'int'>, floating_point=<class 'float'>, boolean=<class 'bool'>, string=<class 'str'>, bytes_=<class 'bytes'>)")


# class TestBaseValueTypes(unittest.TestCase):
#     def setUp(self):
#         self.base_value_types = BaseValueTypes()

#     def test_init_with_str(self):
#         self.assertEqual(self.base_value_types.integer, int)
#         self.assertEqual(self.base_value_types.floating_point, float)
#         self.assertEqual(self.base_value_types.boolean, bool)
#         self.assertEqual(self.base_value_types.string, str)
#         self.assertEqual(self.base_value_types.bytes_, bytes)
#         self.assertEqual(self.base_value_types.number, int | float)
#         self.assertEqual(self.base_value_types.text, str | bytes | bool | None)
#         # self.assertEqual(self.base_value_types._all, int | float | str | bytes | bool | None)

#     def test_base_value_type_has_slots(self):
#         for slot in self.base_value_types.__slots__:
#             self.assertTrue(hasattr(self.base_value_types, slot))

#     def test_base_value_type_has_all_slots(self):
#         self.assertEqual(
#             self.base_value_types.__slots__, (
#                 "integer", "floating_point", "boolean", "string", "bytes_", "number", "text", # "_all"
#             )
#         )

#     def test_base_value_type_has_no_weakref_slot(self):
#         self.assertFalse(hasattr(self.base_value_types, "__weakref__"))

#     def test_base_value_type_has_no_dict(self):
#         self.assertFalse(hasattr(self.base_value_types, "__dict__"))

#     def test_base_value_type_repr(self):
#         self.maxDiff = None
#         self.assertEqual(
#             repr(self.base_value_types), "BaseValueTypes(integer=<class 'int'>, floating_point=<class 'float'>, boolean=<class 'bool'>, string=<class 'str'>, bytes_=<class 'bytes'>, number=int | float, text=str | bytes | bool | None)"
#         )

#     def _test_base_value_type_all_property(self):
#         self.assertEqual(self.base_value_types.all, int | float | str | bytes | bool | None)



# class TestBaseContainerTypes(unittest.TestCase):
#     def setUp(self):
#         self.base_container_types = BaseContainerType
        
#     def test_init_with_str(self):
#         self.assertEqual(self.base_container_types.dictionary, dict)
#         self.assertEqual(self.base_container_types.list_, list)
#         self.assertEqual(self.base_container_types.tuple_, tuple)
#         self.assertEqual(self.base_container_types.set_, set)
#         self.assertEqual(self.base_container_types.frozenset_, frozenset)
#         self.assertEqual(self.base_container_types.linear, tuple | list | set | frozenset)
#         self.assertEqual(self.base_container_types.named, dict)

#     def test_base_container_type_has_slots(self):
#         for slot in self.base_container_types.__slots__:
#             self.assertEqual(hasattr(self.base_container_types, slot), True)

#     def test_base_container_type_has_all_slots(self):
#         self.assertEqual(
#             self.base_container_types.__slots__, ('dictionary', 'list_', 'tuple_', 'set_', 'frozenset_', 'named', 'linear')
#         )

#     def test_base_container_type_has_no_weakref_slot(self):
#         self.assertFalse(hasattr(self.base_container_types, "__weakref__"))

#     def test_base_container_type_has_no_dict(self):
#         self.assertFalse(hasattr(self.base_container_types, "__dict__"))

#     def test_base_container_type_repr(self):
#         self.maxDiff = None
#         self.assertEqual(
#             repr(self.base_container_types), "BaseContainerTypes(dictionary=<class 'dict'>, list_=<class 'list'>, tuple_=<class 'tuple'>, set_=<class 'set'>, frozenset_=<class 'frozenset'>, named=<class 'dict'>, linear=list | tuple | set | frozenset)"
#         )

#     def test_base_container_type_all_property(self):
#         self.assertEqual(self.base_container_types.all, dict | list | tuple | set | frozenset)

#     def test_base_container_type_aliases(self):
#         self.maxDiff = None
#         self.assertEqual(
#             self.base_container_types.aliases, {
#                 self.base_container_types.dictionary: ("Dictionary", "dictionary", "DICTIONARY", "Dict", "dict", "DICT", "DictType", "dict_type", "DICT_TYPE"),
#                 self.base_container_types.list_: ("List", "list", "LIST", "ListType", "list_type", "LIST_TYPE"),
#                 self.base_container_types.tuple_: ("Tuple", "tuple", "TUPLE", "TupleType", "tuple_type", "TUPLE_TYPE"),
#                 self.base_container_types.set_: ("Set", "set", "SET", "SetType", "set_type", "SET_TYPE"),
#                 self.base_container_types.frozenset_: ("FrozenSet", "frozenset", "FROZENSET", "FrozenSetType", "frozenset_type", "FROZENSET_TYPE"),
#                 # self.base_container_types.named: ("Named", "named", "NAMED", "NamedContainer", "named_container", "NAMED_CONTAINER", "NamedContainerType", "named_container_type", "NAMED_CONTAINER_TYPE"),
#                 self.base_container_types.linear: ("Linear", "linear", "LINEAR", "LinearContainer", "linear_container", "LINEAR_CONTAINER", "LinearContainerType", "linear_container_type", "LINEAR_CONTAINER_TYPE"),
#                 self.base_container_types.all: ("BaseContainer", "base_container", "BASE_CONTAINER", "BaseContainerTypes", "base_container_types", "BASE_CONTAINER_TYPES", "BaseContainerType", "base_container_type", "BASE_CONTAINER_TYPE")
#             }
#         )

#     def test_base_container_type_verify_base_container_type(self):
#         self.assertTrue(self.base_container_types._is_container_type(dict()))
#         self.assertTrue(self.base_container_types._is_container_type(list()))
#         self.assertTrue(self.base_container_types._is_container_type(tuple()))
#         self.assertTrue(self.base_container_types._is_container_type(set()))
#         self.assertTrue(self.base_container_types._is_container_type(frozenset()))
#         self.assertTrue(self.base_container_types._is_container_type(dict()))
#         self.assertTrue(self.base_container_types._is_container_type([1,2,3]))
#         self.assertFalse(self.base_container_types._is_container_type(int))
#         self.assertFalse(self.base_container_types._is_container_type(float))
#         self.assertFalse(self.base_container_types._is_container_type(bool))
#         self.assertFalse(self.base_container_types._is_container_type(str))
#         self.assertFalse(self.base_container_types._is_container_type(bytes))
#         self.assertFalse(self.base_container_types._is_container_type(1))
#         self.assertFalse(self.base_container_types._is_container_type(1.0))
#         self.assertFalse(self.base_container_types._is_container_type(True))
#         self.assertFalse(self.base_container_types._is_container_type("test"))
#         self.assertFalse(self.base_container_types._is_container_type(b"test"))
#         self.assertFalse(self.base_container_types._is_container_type(None))
#         self.assertFalse(self.base_container_types._is_container_type(BaseValueTypes))
#         self.assertFalse(self.base_container_types._is_container_type(BaseContainerTypes))
#         self.assertFalse(self.base_container_types._is_container_type(BaseTypesInterface))

#     def test_base_type_interface_init(self):
#         self.maxDiff = None
#         Integer = BaseTypeInterface(
#             aliases=("Integer", "integer", "INTEGER", "Int", "int", "INT", "IntType", "int_type", "INT_TYPE"),
#             super_type="__RESERVED_SYSTEM_INT__",
#             type_class=int,
#             type_var=TypeVar("Integer", bound=int),
#             constraints=int
#         )
#         self.assertEqual(Integer.__slots__, ("aliases", "super_type", "prefix", "suffix", "separator", "type_class", "type_var", "constraints", "_encryption_key"))
#         self.assertEqual(Integer.aliases, ("Integer", "integer", "INTEGER", "Int", "int", "INT", "IntType", "int_type", "INT_TYPE"))

#         self.assertFalse(hasattr(Integer, "__weakref__"))
#         self.assertFalse(hasattr(Integer, "__dict__"))

#         self.assertFalse(Integer.is_container)

#         self.assertEqual(repr(Integer), "BaseTypeInterface(aliases=('Integer', 'integer', 'INTEGER', 'Int', 'int', 'INT', 'IntType', 'int_type', 'INT_TYPE'), super_type='__RESERVED_SYSTEM_INT__', prefix=None, suffix=None, separator=None, type_class=<class 'int'>, type_var=~Integer, constraints=<class 'int'>)")

#         self.assertEqual(Integer._hash_repr(), "2ed75541630ac14c09df9b1f8a29182f373e080faf12136f6f54ee97ec7a9f4d")

#     def test_system_type_pool(self):
# 
#         self.assertEqual(self.system_pool.__slots__, ("Integer", "FloatingPoint", "Boolean", "String", "Bytes", "Dictionary", "List", "Tuple", "Set", "FrozenSet"))

#     def test_system_type_pool_type_instance(self):
# 
#         int_type = system_pool.Integer
#         self.assertEqual(int_type.__slots__, ("aliases", "super_type", "prefix", "suffix", "separator", "type_class", "type_var", "constraints", "_encryption_key"))
#         self.assertEqual(int_type.aliases, ("Integer", "integer", "INTEGER", "Int", "int", "INT", "IntegerType", "integer_type", "INTEGER_TYPE", "IntType", "int_type", "INT_TYPE"))
#         self.assertEqual(int_type.super_type, "__SYSTEM_RESERVED_INT__")
#         self.assertEqual(int_type.prefix, None)
#         self.assertEqual(int_type.suffix, None)
#         self.assertEqual(int_type.separator, None)
#         self.assertEqual(int_type.type_class, int)

#     def test_system_type_pool_type_instance_repr(self):
#         int_type = BaseTypes().Integer
#         self.assertEqual(repr(int_type), "BaseTypeInterface(aliases=('Integer', 'integer', 'INTEGER', 'Int', 'int', 'INT', 'IntegerType', 'integer_type', 'INTEGER_TYPE', 'IntType', 'int_type', 'INT_TYPE'), super_type='__SYSTEM_RESERVED_INT__', prefix=None, suffix=None, separator=None, type_class=<class 'int'>, type_var=~Integer, constraints=<class 'int'>)")

#     def test_system_type_pool_already_exists(self):
# 
#         self.assertTrue(self.system_pool._already_exists("aliases", "Integer"))
#         self.assertTrue(self.system_pool._already_exists("aliases", "integer"))
#         self.assertTrue(self.system_pool._already_exists("super_type", "__SYSTEM_RESERVED_INT__"))
#         self.assertRaises(GroupBaseTypeException, system_pool._already_exists, "aliases", "I")
    
#     def test_system_type_pool_get_type(self):
# 
#         self.assertEqual(self.system_pool._get_type("aliases", "Integer"), system_pool.Integer)
#         self.assertEqual(self.system_pool._get_type("aliases", "integer"), system_pool.Integer)
#         self.assertEqual(self.system_pool._get_type("super_type", "__SYSTEM_RESERVED_INT__"), system_pool.Integer)
#         self.assertRaises(GroupBaseTypeException, system_pool._get_type, "aliases", "I")

#     def test_system_type_pool_get_type_from_alias(self):
# 
#         self.assertEqual(self.system_pool._get_type_from_alias("Integer"), system_pool.Integer.type_class)
#         self.assertEqual(self.system_pool._get_type_from_alias("integer"), system_pool.Integer.type_class)
#         self.assertEqual(self.system_pool._get_type_from_alias("INTEGER"), system_pool.Integer.type_class)
#         self.assertEqual(self.system_pool._get_type_from_alias("Int"), system_pool.Integer.type_class)
#         self.assertEqual(self.system_pool._get_type_from_alias("int"), system_pool.Integer.type_class)
#         self.assertEqual(self.system_pool._get_type_from_alias("INT"), system_pool.Integer.type_class)

 
 
    def setUp(self):
        self.system_pool = BaseTypes

    def test_system_type_pool_get_type_from_alias_raises(self):
        self.assertRaises(GroupBaseTypeException, self.system_pool._get_type_from_alias, "I")

    
    def test_system_type_pool_validate_types(self):

        self.assertTrue(self.system_pool._validate_types())

    def test_system_type_pool_all(self):

        self.assertEqual(self.system_pool.all(), int | float | bool | str | bytes | dict | list | tuple | set | frozenset | None)
        self.assertEqual(self.system_pool.all(type_="value"), int | float | bool | str | bytes | None)

    def test_system_type_pool_hash_public(self):

        self.assertEqual(self.system_pool._hash_public_slots(), "0a8f54ea737cc48026bb0543423e017d15ff89b7f12e7936fb67aa570052496e")

    def test_system_type_pool_hash_private(self):

        self.assertEqual(self.system_pool._hash_private_slots(), None)

    def test_system_type_pool_hash_repr(self):

        self.assertEqual(self.system_pool._hash_repr(), "83c810371a6c7fde5626f7fd568efa9bf81a00edeff55ac7a53b785f8eebd4f6")

    def test_system_type_pool_repr(self):
        self.maxDiff = None

        self.assertEqual(repr(self.system_pool), "_BaseTypes(Integer=BaseTypeInterface(aliases=('Integer', 'integer', 'INTEGER', 'Int', 'int', 'INT', 'IntegerType', 'integer_type', 'INTEGER_TYPE', 'IntType', 'int_type', 'INT_TYPE'), super_type='__SYSTEM_RESERVED_INT__', prefix=None, suffix=None, separator=None, type_class=<class 'int'>, type_var=~Integer, constraints=<class 'int'>), FloatingPoint=BaseTypeInterface(aliases=('FloatingPoint', 'floating_point', 'FLOATING_POINT', 'Float', 'float', 'FLOAT', 'FloatingPointType', 'floating_point_type', 'FLOATING_POINT_TYPE', 'FloatType', 'float_type', 'FLOAT_TYPE'), super_type='__SYSTEM_RESERVED_FLOAT__', prefix=None, suffix=None, separator=None, type_class=<class 'float'>, type_var=~FloatingPoint, constraints=<class 'float'>), Boolean=BaseTypeInterface(aliases=('Boolean', 'boolean', 'BOOLEAN', 'Bool', 'bool', 'BOOL', 'BooleanType', 'boolean_type', 'BOOLEAN_TYPE', 'BoolType', 'bool_type', 'BOOL_TYPE'), super_type='__SYSTEM_RESERVED_BOOL__', prefix=None, suffix=None, separator=None, type_class=<class 'bool'>, type_var=~Boolean, constraints=<class 'bool'>), String=BaseTypeInterface(aliases=('String', 'string', 'STRING', 'Str', 'str', 'STR', 'StringType', 'string_type', 'STRING_TYPE', 'StrType', 'str_type', 'STR_TYPE'), super_type='__SYSTEM_RESERVED_STR__', prefix=None, suffix=None, separator=None, type_class=<class 'str'>, type_var=~String, constraints=<class 'str'>), Bytes=BaseTypeInterface(aliases=('Bytes', 'bytes', 'BYTES', 'BytesType', 'bytes_type', 'BYTES_TYPE'), super_type='__SYSTEM_RESERVED_BYTES__', prefix=None, suffix=None, separator=None, type_class=<class 'bytes'>, type_var=~Bytes, constraints=<class 'bytes'>), Dictionary=BaseTypeInterface(aliases=('Dictionary', 'dictionary', 'DICTIONARY', 'Dict', 'dict', 'DICT', 'DictType', 'dict_type', 'DICT_TYPE'), super_type='__SYSTEM_RESERVED_DICT__', prefix='{', suffix='}', separator=',', type_class=<class 'dict'>, type_var=~Dictionary, constraints=<class 'dict'>), List=BaseTypeInterface(aliases=('List', 'list', 'LIST', 'ListType', 'list_type', 'LIST_TYPE'), super_type='__SYSTEM_RESERVED_LIST__', prefix='[', suffix=']', separator=',', type_class=<class 'list'>, type_var=~List, constraints=<class 'list'>), Tuple=BaseTypeInterface(aliases=('Tuple', 'tuple', 'TUPLE', 'TupleType', 'tuple_type', 'TUPLE_TYPE'), super_type='__SYSTEM_RESERVED_TUPLE__', prefix='(', suffix=')', separator=',', type_class=<class 'tuple'>, type_var=~Tuple, constraints=<class 'tuple'>), Set=BaseTypeInterface(aliases=('Set', 'set', 'SET', 'SetType', 'set_type', 'SET_TYPE'), super_type='__SYSTEM_RESERVED_SET__', prefix='{', suffix='}', separator=',', type_class=<class 'set'>, type_var=~Set, constraints=<class 'set'>), FrozenSet=BaseTypeInterface(aliases=('FrozenSet', 'frozenset', 'FROZENSET', 'FrozenSetType', 'frozenset_type', 'FROZENSET_TYPE'), super_type='__SYSTEM_RESERVED_FROZENSET__', prefix='{', suffix='}', separator=',', type_class=<class 'frozenset'>, type_var=~FrozenSet, constraints=<class 'frozenset'>))")

    def test_system_base_type_interface_hash_public(self):

        integer = self.system_pool.Integer
        self.assertEqual(integer._hash_public_slots(), "e87c23c3af923f131a1f85996611d5a7a932832e04d83c2ad2ab831b572f2618")