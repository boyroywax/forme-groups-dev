
from typing import Optional, overload, Union
import ipfs_api


__IPFS_DEFAULT_URL__ = '/ip4/127.0.0.1/tcp/5001'


class IPFSCID:
    cid: Optional[str] = None

    def __init__(self):
        self.ipfs_client = ipfs_api.ipfshttpclient.connect(
            __IPFS_DEFAULT_URL__
        )

    @overload
    def generate_cid(self, data: bytes) -> str: ...

    @overload
    def generate_cid(self, data: str) -> str: ...

    def generate_cid(self, data: Union[bytes, str]) -> str:
        if isinstance(data, bytes):
            res = self.ipfs_client.add_bytes(data)
            print(res)
            cid = res
            if self.ipfs_client.cat(cid) == data:
                self.cid = cid
                return cid
        elif isinstance(data, str):
            cid = self.ipfs_client.add_str(data)
            print(cid)
            # if self.ipfs_client.cat(cid) == data:
            self.cid = cid
            return cid
        else:
            raise ValueError("CID verification failed")