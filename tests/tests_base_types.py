import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.base.types import BaseTypes
from src.groups.base.exceptions import GroupBaseTypeException

class TestBaseTypes(unittest.TestCase):
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