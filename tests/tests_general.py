"""Tests for general functionality of the app."""

import unittest
import sys
import os

# sys.path.append('/Users/j/Documents/Forme/code/forme-groups-python-3-12')

from app.src import App
from app.src.base import BaseInterface


class TestsGeneral(unittest.TestCase):
    """Gereral tests."""

    def setUp(self):
        self.app = App()

    def test_app_run(self):
        """Test the app run method."""
        self.app.run()
        # self.debug = True
        # if self.debug:
        #     print("\n"+sys.version)
        #     print("\n"+str(sys.version_info))
        #     print("\n"+os.getcwd())
        #     print("\n"+__file__)
        #     print("\n"+os.path.dirname(__file__))
        #     print("\n"+os.path.dirname(os.path.dirname(__file__)))
        #     print("\n"+os.name)
        #     print("\n"+repr(os.environ.items()))
        #     print("\n"+"Hello world!")
        self.assertIsInstance(self.app, App)

    def test_app_create_types(self):
        """Test the app create_types method."""
        self.assertTrue(self.app.create_types())

    def test_app_create_types2(self):
        """Test the app create_types2 method."""
        self.assertTrue(self.app.create_types2())

    def test_app_value(self):
        """Test the value class."""
        value: BaseInterface = BaseInterface(1)
        self.assertIsInstance(value, BaseInterface)
        self.assertIsInstance(value._value, int)
