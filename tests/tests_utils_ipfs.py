import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.utils.ipfs import IPFS


class TestIPFS(unittest.TestCase):
    def test_init(self):
        ipfs = IPFS()
        self.assertEqual(ipfs.client.my_id(), ipfs.get_ipfs_peer_id())