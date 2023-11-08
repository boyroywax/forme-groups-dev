
import ipfs_api

__IPFS_DEFAULT_URL__ = '/ip4/127.0.0.1/tcp/5001'


class IPFSCID:
    def __init__(self):
        self.ipfs_client = ipfs_api.ipfshttpclient.connect(__IPFS_DEFAULT_URL__)

    def generate_cid(self, data):
        res = self.ipfs_client.add_bytes(data)
        print(res)
        cid = res
        if self.ipfs_client.cat(cid) == data:
            return cid
        else:
            raise ValueError("CID verification failed")
