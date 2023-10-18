import unittest
import sys

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from src.groups.base.container import BaseContainer, _contains_sub_container
from src.groups.base.value import BaseValue
from src.groups.base.exceptions import GroupBaseContainerException


class TestBaseContainer(unittest.TestCase):
    def test_init_with_tuple(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))
        self.assertEqual(container.type, "tuple")

    def test_init_with_dict(self):
        container = BaseContainer({"a": 1, "b": 2, "c": 3}, "dictionary")
        self.assertEqual(container.items, (BaseValue("a"), BaseValue(1), BaseValue("b"), BaseValue(2), BaseValue("c"), BaseValue(3)))

    def test_init_with_list(self):
        container = BaseContainer([1, 2, 3], "list")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_init_with_set(self):
        container = BaseContainer({1, 2, 3}, "set")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_init_with_frozenset(self):
        container = BaseContainer(frozenset({1, 2, 3}), "frozenset")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_iter(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual([item for item in iter(container)], [BaseValue(1), BaseValue(2), BaseValue(3)])

    def test_str(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(str(container), "(1, 2, 3)")

    def test_repr(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(repr(container), "BaseContainer(items=(BaseValue(value=1, type=int), BaseValue(value=2, type=int), BaseValue(value=3, type=int)), type=tuple)")

    def test_type(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(container.type, "tuple")

    def test_has_slots(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertEqual(container.__slots__, ('_items', '_type'))

    def test_create_large_container(self):
        container = BaseContainer([i for i in range(10000)])
        self.assertEqual(len(container.items), 10000)
    
    def test_init_with_multiple_containers(self):
        self.assertRaises(GroupBaseContainerException, BaseContainer, (1, 2, 3), [1, 2, 3])

    def test_init_with_improper_type(self):
        self.assertRaises(GroupBaseContainerException, BaseContainer, (1, 2, 3), 1)

    def test_init_with_improper_type2(self):
        self.assertRaises(GroupBaseContainerException, BaseContainer, (1, 2, 3), "int")

    def test_str_with_dict(self):
        container = BaseContainer({"a": 1, "b": 2, "c": 3}, "dictionary")
        self.assertEqual(str(container), "{'a': 1, 'b': 2, 'c': 3}")

    def test_init_with_mismatched_types_will_work(self):
        container = BaseContainer((1, 2, 3), "set")
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_hash_pack_unpack(self):
        container = BaseContainer((1, 2, 3), "tuple")
        hash_tree = container._hash_package()
        self.assertEqual(hash_tree.root(), '1083b34843b3e9d41485d4821b19731777c637f09f81ae3f93d12280032ed5a1')

    def test_hash_pack_verify(self):
        container = BaseContainer((1, 2, 3), "tuple")
        hash_repre_item_one = container.items[0]
        print(hash_repre_item_one)
        self.assertTrue(container._verify_item(item=hash_repre_item_one))

    def test_hash_pack_unpack2(self):
        container = BaseContainer((1, 2, 3), "tuple")
        hash_str = container._hash_repr()
        self.assertEqual(hash_str, '6c55c905bbb40515f339893e503bf2241b6f8ebbf4545447e67560fcb147c7fa')
    
    def test_contains_sub_container(self):
        container = BaseContainer((1, 2, 3), "tuple")
        self.assertFalse(_contains_sub_container(container.items))

    def test_contains_sub_container2(self):
        self.assertTrue(_contains_sub_container, (1, 2, [3, 4, 5]))

    def test_creating_container_with_sub_container(self):
        self.assertRaises(GroupBaseContainerException, BaseContainer, (1, 2, [3, 4, 5]), "tuple")

    def test_creating_container_with_uneven_items_for_type_dict(self):
        container_dict_invalid = BaseContainer(("a", 1, "b", 2, "c"), "dictionary")
        self.assertRaises(Exception, f'{container_dict_invalid}')
