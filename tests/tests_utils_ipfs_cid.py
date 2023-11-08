import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.utils.cid import IPFSCID

class TestIPFSCID(unittest.TestCase):
    def test_init(self):
        ipfs_cid = IPFSCID()
        self.assertIsNotNone(ipfs_cid.ipfs_client)

    def test_generate_cid(self):
        ipfs_cid = IPFSCID()
        data = b"test"
        cid = ipfs_cid.generate_cid(data)
        self.assertEqual(cid, "QmRf22bZar3WKmojipms22PkXH1MZGmvsqzQtuSvQE3uhm")