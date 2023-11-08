import unittest
import sys

sys.path.append("../forme-groups-python-3-12/")
from src.groups.utils.ipfs import IPFS


class TestIPFS(unittest.TestCase):
    def setUp(self):
        self.ipfs = IPFS()

    def test_init(self):
        ipfs = IPFS()
        # self.assertIsNotNone(ipfs.get_ipfs_client_id())

    # def test_status(self):
    #     ipfs = IPFS()
    #     self.assertEqual(ipfs.status(), True)

    # def test_add_bytes(self):
    #     ipfs = IPFS()
    #     self.assertEqual(ipfs.add_bytes(b'test'), "QmRf22bZar3WKmojipms22PkXH1MZGmvsqzQtuSvQE3uhm")

    # def test_add_string(self):
    #     ipfs = IPFS()
    #     self.assertEqual(ipfs.add_str("test"), "QmRf22bZar3WKmojipms22PkXH1MZGmvsqzQtuSvQE3uhm")

    # def test_compute_ipfs_hash_from_bytes(self):
    #     ipfs = IPFS()
    #     self.assertEqual(ipfs.compute_ipfs_hash_from_bytes(b'test'), "QmRf22bZar3WKmojipms22PkXH1MZGmvsqzQtuSvQE3uhm")

    # def test_compute_ipfs_cid(self):
    #     ipfs = IPFS()
    #     self.assertEqual(ipfs.compute_ipfs_cid(b'test'), "QmRf22bZar3WKmojipms22PkXH1MZGmvsqzQtuSvQE3uhm")

    # def test_publish(self):
    #     ipfs = IPFS()
    #     self.assertEqual(ipfs.publish('state-test.json'), "QmWYgCstdspqdkMoLXfPe4RtyVgrWhU4btCcygQBYaohhU")

    # def test_calculate_cid(self):
    #     ipfs = IPFS()
    #     self.assertEqual(ipfs.calculate_cid(b'test'), "QmRf22bZar3WKmojipms22PkXH1MZGmvsqzQtuSvQE3uhm")


