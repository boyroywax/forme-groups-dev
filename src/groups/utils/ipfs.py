
from attr import define
import ipfs_api
import json



@define(slots=True)
class IPFS:
    client = ipfs_api
    # client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5002/http/')

    def get_ipfs_peer_id(self):
        return self.client.my_id()



