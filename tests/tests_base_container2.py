import unittest
import sys

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.exceptions import GroupBaseContainerException
from app.src.base.container2 import BaseContainer
from app.src.base.value import BaseValue


class TestBaseContainer(unittest.TestCase):
    def test_init_with_tuple(self):
        container = BaseContainer((BaseValue(1), BaseValue(2), BaseValue(3)), tuple)
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_init_with_dict(self):
        container = BaseContainer({"a": 1, "b": 2, "c": 3})
        self.assertEqual(container.items, (BaseValue("a"), BaseValue(1), BaseValue("b"), BaseValue(2), BaseValue("c"), BaseValue(3)))

    def test_init_with_list(self):
        container = BaseContainer([1, 2, 3])
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

    def test_init_with_set(self):
        container = BaseContainer({1, 2, 3})
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))
        self.assertEqual(container.type, set)
    
    def test_init_with_incorrect_type(self):
        with self.assertRaises(GroupBaseContainerException):
            BaseContainer(1)

    

