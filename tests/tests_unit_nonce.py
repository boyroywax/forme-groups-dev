import unittest
import sys

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")

from src.groups.unit.nonce import Nonce
from src.groups.base.container import BaseContainer
from src.groups.base.exceptions import GroupBaseException


class TestUnitNonce(unittest.TestCase):
    def setUp(self):
        self.base_contaiiner = BaseContainer((0, ), "tuple")
        self.nonce = Nonce(self.base_contaiiner)

    def test_str(self):
        self.assertEqual(str(self.nonce), '0')

    def test_get_active(self):
        self.assertEqual(self.nonce._get_active().value, 0)

    def test_repr(self):
        self.assertEqual(repr(self.nonce), 'Nonce(chain=BaseContainer(items=(BaseValue(value=0, type=int),), type=tuple))')

    def test_nonce_str(self):
        base_container_two = BaseContainer(("zero", "zero", "one"), "tuple")
        nonce_two = Nonce(base_container_two)
        self.assertEqual(str(nonce_two), 'zero.zero.one')

    def test_incompatible_nonce_type(self):
        base_container_three = BaseContainer((b"test", ), "tuple")
        self.assertRaises(GroupBaseException, Nonce, base_container_three)

    def test_next_active_int(self):
        self.assertEqual(str(self.nonce._next_active()), '1')

    def test_next_active_value_str(self):
        base_container_four = BaseContainer(("zero", "zero", "one"), "tuple")
        nonce_four = Nonce(base_container_four)
        self.assertEqual(str(nonce_four._next_active()), 'onf')

    def test_next_active_value_str_z(self):
        base_container_five = BaseContainer(("zero", "zero", "one", "z"), "tuple")
        nonce_five = Nonce(base_container_five)
        self.assertEqual(str(nonce_five._next_active()), 'za')

    def test_next_active_chain(self):
        self.assertEqual(str(self.nonce._next_active_chain()), '(1,)')

    def test_next_active_nonce(self):
        self.assertEqual(str(self.nonce._next_active_nonce()), '1')

    def test_next_active_nonce_str(self):
        base_container_six = BaseContainer(("zero", "zero", "one"), "tuple")
        nonce_six = Nonce(base_container_six)
        self.assertEqual(str(nonce_six._next_active_nonce()), 'zero.zero.onf')