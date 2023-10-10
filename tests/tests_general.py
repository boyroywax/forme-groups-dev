"""Tests for general functionality of the app."""

import unittest
import sys
import os

# sys.path.append('/Users/j/Documents/Forme/code/forme-groups-python-3-12')

# from app.src import App
from app.src.base import BaseInterface


class TestsGeneral(unittest.TestCase):
    """Gereral tests."""

    def setUp(self):
        self.app = App()
