import unittest
from unittest.mock import Mock
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.unit.credential import Credential
from src.groups.base.container import BaseContainer

class TestCredential(unittest.TestCase):
    def test_credential_creation(self):
        credential = Credential()
        self.assertIsNone(credential.credential)

    def test_credential_with_container(self):
        container_mock = Mock(spec=BaseContainer)
        credential = Credential(credential=container_mock)
        self.assertEqual(credential.credential, container_mock)
