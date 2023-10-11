import unittest
import sys

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.container import BaseContainer
from app.src.base.value import BaseValue


class TestBaseContainer(unittest.TestCase):
    def test_init_with_tuple(self):
        container = BaseContainer((1, 2, 3))
        self.assertEqual(container.items, (BaseValue(1), BaseValue(2), BaseValue(3)))

