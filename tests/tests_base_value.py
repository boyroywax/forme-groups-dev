import unittest
import sys
import random
import uuid

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")
from app.src.base.value import BaseValue
from app.src.base.exceptions import GroupBaseValueException


class TestBaseValue(unittest.TestCase):
    def test_init_with_int(self):
        value = BaseValue(1)
        self.assertEqual(value.value, 1)

    def test_init_with_float(self):
        value = BaseValue(1.0)
        self.assertEqual(value.value, 1.0)

    def test_init_with_bool(self):
        value = BaseValue(True)
        self.assertEqual(value.value, True)

    def test_init_with_str(self):
        value = BaseValue("hello")
        self.assertEqual(value.value, "hello")

    def test_init_with_none(self):
        value = BaseValue(None)
        self.assertEqual(value.value, None)

    def test_init_with_list(self):
        try:
            value = BaseValue([1, 2, 3])
        except GroupBaseValueException:
            self.assertTrue(True)
        self.assertRaises(GroupBaseValueException, BaseValue, [1, 2, 3])
    
    def test_init_with_dict(self):
        try:
            value = BaseValue({"a": 1, "b": 2, "c": 3})
        except GroupBaseValueException:
            self.assertTrue(True)
        self.assertRaises(GroupBaseValueException, BaseValue, {"a": 1, "b": 2, "c": 3})

    def test_init_with_set(self):
        try:
            value = BaseValue({1, 2, 3})
        except GroupBaseValueException:
            self.assertTrue(True)
        self.assertRaises(GroupBaseValueException, BaseValue, {1, 2, 3})

    def test_init_with_frozenset(self):
        try:
            value = BaseValue(frozenset({1, 2, 3}))
        except GroupBaseValueException:
            self.assertTrue(True)
        self.assertRaises(GroupBaseValueException, BaseValue, frozenset({1, 2, 3}))

    def test_init_with_tuple(self):
        try:
            value = BaseValue((1, 2, 3))
        except GroupBaseValueException:
            self.assertTrue(True)
        self.assertRaises(GroupBaseValueException, BaseValue, (1, 2, 3))

    def test_init_with_object(self):
        class Test:
            def __init__(self):
                pass
        try:
            value = BaseValue(Test())
        except GroupBaseValueException:
            self.assertTrue(True)
        self.assertRaises(GroupBaseValueException, BaseValue, Test())

    def test_init_with_bytes(self):
        value = BaseValue(b"hello")
        self.assertEqual(value.value, b"hello")

    def test_init_with_BaseValue(self):
        try:
            value = BaseValue(BaseValue(1))
        except GroupBaseValueException:
            self.assertTrue(True)
        self.assertRaises(GroupBaseValueException, BaseValue, BaseValue(1))

    def test_init_with_BaseValue_with_int(self):
        value = BaseValue(BaseValue(1).value)
        self.assertEqual(value.value, 1)

    def test_init_with_container(self):
        self.assertRaises(GroupBaseValueException, BaseValue, [1, 2, 3])

    def test_base_value_has_slots(self):
        value = BaseValue(1)
        self.assertEqual(value.__slots__, ('_value', ))

    def test_base_value_is_frozen(self):
        value = BaseValue(1)
        self.assertRaises(AttributeError, setattr, value, "value", 2)

    def test_base_value_str(self):
        value = BaseValue(1)
        self.assertEqual(str(value), "1")

    def test_base_value_repr(self):
        values = [1, 1.0, True, "hello", None, b"hello"]
        for value in values:
            self.assertEqual(repr(BaseValue(value)), f"BaseValue(value={repr(value)}, type={type(value).__name__})")

    def test_base_value_eq(self):
        value = BaseValue(1)
        self.assertTrue(value == BaseValue(1))

    def test_base_value_eq_with_different_value(self):
        value = BaseValue(1)
        self.assertFalse(value == BaseValue(2))

    def test_base_value_eq_with_different_type(self):
        value = BaseValue(1)
        self.assertFalse(value == BaseValue("1"))

    def test_base_value_hash(self):
        value = BaseValue(1)
        print(repr(value))
        self.assertEqual(value._hash_repr(), '5176a0db25fa8911b84f16b90d6c02d56d0c983122bc26fd137713aa0ede123f')

    def test_base_value_hash_with_different_value(self):
        value = BaseValue(1)
        self.assertNotEqual(value._hash_repr(), BaseValue(2)._hash_repr())

    def test_base_value_peek_value(self):
        value = BaseValue(1)
        self.assertEqual(BaseValue._peek_value(value), 1)

    def test_base_value_peek_value_with_unit_value_types(self):
        values = [1, 1.0, True, "hello", None, b"hello"]
        for value in values:
            based_value = BaseValue(value)
            self.assertEqual(BaseValue._peek_value(based_value), value)

    def test_base_value_peek_value_with_containers(self):
        self.assertRaises(GroupBaseValueException, BaseValue._peek_value, [1, 2, 3])
        self.assertRaises(GroupBaseValueException, BaseValue._peek_value, {1, 2, 3})
        self.assertRaises(GroupBaseValueException, BaseValue._peek_value, (1, 2, 3))
        self.assertRaises(GroupBaseValueException, BaseValue._peek_value, {"a": 1, "b": 2, "c": 3})
        self.assertRaises(GroupBaseValueException, BaseValue._peek_value, frozenset({1, 2, 3}))

    def test_base_value_hash_with_str(self):
        value = BaseValue("hello")
        self.assertEqual(value._hash_repr(), 'cbdba380edb6b63b8e0dc697952a7d4e420fc1ece0542bd22968345234ad4565')

    def test_base_value_get_type_str(self):
        value = BaseValue(1)
        self.assertEqual(value.get_type_str(), "int")

    def test_base_value_get_type_str_with_str(self):
        value = BaseValue("hello")
        self.assertEqual(value.get_type_str(), "str")

    def test_base_value_force_type(self):
        value = BaseValue(1)
        self.assertEqual(BaseValue._force_type(value, "<class 'str'>"), BaseValue("1"))

    def test_base_value_force_type_with_str(self):
        value = BaseValue("hello")
        self.assertRaises(GroupBaseValueException, BaseValue._force_type, value, type(int).__name__)

    def test_base_value_force_type_with_int_one_is_true(self):
        value = BaseValue(1)
        result = BaseValue._force_type(value, "bool")
        self.assertEqual(result, BaseValue(True))

    def test_base_value_force_type_with_bool_fails(self):
        value = BaseValue(True)
        self.assertEqual(BaseValue._force_type(value, "int"), BaseValue(1))

    def test_base_value_force_type_with_none_fails(self):
        value = BaseValue(None)
        self.assertRaises(GroupBaseValueException, BaseValue._force_type, value, "int")

    def test_base_value_force_type_with_bytes_fails(self):
        value = BaseValue(b"hello")
        self.assertRaises(GroupBaseValueException, BaseValue._force_type, value, "int")

    def test_base_value_force_type_with_float_to_int_whole_number(self):
        value = BaseValue(1.6)
        result = BaseValue._force_type(value, "int")
        self.assertEqual(result, BaseValue(1))

    def test_base_value_force_type_with_float_to_str(self):
        value = BaseValue(1.6)
        self.assertEqual(BaseValue._force_type(value, "str"), BaseValue("1.6"))

    def test_base_value_force_type_with_float_to_bool(self):
        value = BaseValue(1.6)
        self.assertEqual(BaseValue._force_type(value, "bool"), BaseValue(True))

    def test_base_value_force_type_with_float_to_bytes(self):
        value = BaseValue(1.6)
        self.assertEqual(BaseValue._force_type(value, "bytes"), BaseValue(b'\xcd\xcc\xcc?'))

    def test_base_value_force_type_with_float_to_none(self):
        value = BaseValue(1.6)
        self.assertEqual(BaseValue._force_type(value, "NoneType"), BaseValue(None))

    def test_base_value_init_with_dict(self):
        self.assertRaises(GroupBaseValueException, BaseValue, {"a": 1, "b": 2, "c": 3})

    def test_base_value_init_with_list(self):
        self.assertRaises(GroupBaseValueException, BaseValue, [1, 2, 3])

    def test_base_value_init_with_set(self):
        self.assertRaises(GroupBaseValueException, BaseValue, {1, 2, 3})

    def test_base_value_init_with_frozenset(self):
        self.assertRaises(GroupBaseValueException, BaseValue, frozenset({1, 2, 3}))

    def test_base_value_init_with_tuple(self):
        self.assertRaises(GroupBaseValueException, BaseValue, (1, 2, 3))

    def test_base_value_init_with_object(self):
        class Test:
            def __init__(self):
                pass
        self.assertRaises(GroupBaseValueException, BaseValue, Test())

    def test_base_value_force_type_str_to_int(self):
        value = BaseValue("1")
        self.assertEqual(BaseValue._force_type(value, "int"), BaseValue(1))

    def test_base_value_force_type_str_to_float(self):
        value = BaseValue("1.6")
        self.assertEqual(BaseValue._force_type(value, "float"), BaseValue(1.6))

    def test_base_value_force_type_str_to_bool(self):
        value = BaseValue("True")
        self.assertEqual(BaseValue._force_type(value, "bool"), BaseValue(True))

    def test_base_value_force_type_str_to_bytes(self):
        value = BaseValue("hello")
        self.assertEqual(BaseValue._force_type(value, "bytes"), BaseValue(b"hello"))

    def test_base_value_force_type_int_to_bytes(self):
        value = BaseValue(1)
        self.assertEqual(BaseValue._force_type(value, "bytes"), BaseValue(b'\x01'))
    
    def test_base_value_force_type_float_to_bytes(self):
        value = BaseValue(1.6)
        self.assertEqual(BaseValue._force_type(value, "bytes"), BaseValue(b'\xcd\xcc\xcc?'))

    def test_base_value_force_type_bool_to_bytes(self):
        value = BaseValue(True)
        self.assertEqual(BaseValue._force_type(value, "bytes"), BaseValue(b'\x01'))

    def test_base_value_force_type_bool_to_bytes_with_false(self):
        value = BaseValue(False)
        self.assertEqual(BaseValue._force_type(value, "bytes"), BaseValue(b'\x00'))

    def test_non_base_value_force_type(self):
        self.assertEqual(BaseValue._force_type(1, "int"), BaseValue(1))

    def test_force_type_same_as_input(self):
        value = BaseValue(1)
        self.assertEqual(BaseValue._force_type(value, "int"), BaseValue(1))
        
    def test_base_value_hash_with_bool(self):
        value = BaseValue(True)
        self.assertEqual(value._hash_repr(), 'da1fd978d5160bcb95764a4a7b7d3f6649a0d1e111b0d393339afea675d352b4')

    def test_base_value_get_type_str_with_bool(self):
        value = BaseValue(True)
        self.assertEqual(value.get_type_str(), "bool")

    def test_base_value_get_type_str_with_none(self):
        value = BaseValue(None)
        self.assertEqual(value.get_type_str(), "NoneType")

    def test_base_value_get_type_str_with_bytes(self):
        value = BaseValue(b"hello")
        self.assertEqual(value.get_type_str(), "bytes")

    def test_base_value_get_type_str_with_float(self):
        value = BaseValue(1.6)
        self.assertEqual(value.get_type_str(), "float")

    def test_base_value_get_type_str_with_object(self):
        class Test:
            def __init__(self):
                pass
        self.assertRaises(GroupBaseValueException, BaseValue, Test)

    def test_init_n_base_values(self):
        for i in range(10000):
            values = [
                random.randint(0, 10000000000),
                random.randbytes(256),
                random.choice([True, False]),
                random.random(),
                None,
                str(uuid.uuid4())
            ]
            random_value = random.choice(values)
            value = BaseValue(random_value)
            self.assertEqual(value.value, random_value)

    def test_hash_time_init_n_base_values(self):
        for i in range(10000):
            values = [
                random.randint(0, 10000000000),
                random.randbytes(256),
                random.choice([True, False]),
                random.random(),
                None,
                str(uuid.uuid4())
            ]
            random_value = random.choice(values)
            value = BaseValue(random_value)
            self.assertEqual(value._hash_repr(), value._hash_repr())

    def test_hash_tree(self):
        value = BaseValue(1)
        # print(value._hash_tree())
        self.assertEqual(value._hash_tree().root(), '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b')
        self.assertEqual(value._hash_tree().levels, (('6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', ), ))
        self.assertEqual(value._hash_repr(), '5176a0db25fa8911b84f16b90d6c02d56d0c983122bc26fd137713aa0ede123f')
        self.assertEqual(value._hash_package().root(), "3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd")
        self.assertEqual(value._hash_package().levels, ((None, '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b'), ('3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd', )))

    def test_hash_public_init_n_base_values(self):
        for i in range(10000):
            values = [
                random.randint(0, 10000000000),
                random.randbytes(256),
                random.choice([True, False]),
                random.random(),
                None,
                str(uuid.uuid4())
            ]
            random_value = random.choice(values)
            value = BaseValue(random_value)
            self.assertEqual(value._hash_public_slots(), value._hash_public_slots())

