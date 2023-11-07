from attr import define
import ipfs_api
# import py_ipfs
# import ipfshttpclient2
import json
import hashlib
import base58
import multihash
import multicodec
import varint
import multibase
from multiformats_cid import make_cid, CIDv0, CIDv1, cid
from cbor2 import dumps, loads
from binascii import hexlify
from typing import Iterable
from io import BytesIO
from ipfs_cid import cid_sha256_hash_chunked, cid_sha256_wrap_digest, cid_sha256_unwrap_digest
from .crypto import MerkleTree, Leaves, SHA256Hash
# import pymerkle

# __IPFS_DEFAULT_URL__ = '/ip4/127.0.0.1/tcp/5541/http/'
__IPFS_DEFAULT_URL__ = '/ip4/127.0.0.1/tcp/5001'

@define(slots=True)
class IPFS:
    client = ipfs_api.ipfshttpclient
    # client = ipfshttpclient2.connect('/ip4/127.0.0.1/tcp/5001/http/')

    def connect_client(self):
        return self.client.connect(__IPFS_DEFAULT_URL__)
    
    def psuedo_connect_client(self):
        return self.client.connect()

    def get_ipfs_client_id(self):
        print(self.client.id())
        return self.client.id()

    # def status(self):
    #     return self.client.is_ipfs_running()

    def publish(self, file: str):
        with self.connect_client() as c:
            res = c.add(file)['Hash']
            print(res)
            return res
        # return self.client.publish(file)

    def add_bytes(self, data: bytes):
        with self.client.connect(__IPFS_DEFAULT_URL__) as c:
            return c.add_bytes(data)

    def add_str(self, string: str):
        with self.client.connect(__IPFS_DEFAULT_URL__) as c:
            return c.add_str(string)

    def add_json(self, json_obj: dict):
        return self.client.add_json(json_obj)

    @staticmethod
    def compute_ipfs_hash_from_bytes(data: bytes):

        # print(hexlify(hashlib.sha256(dumps(data)).digest()))
        sha256_1 = SHA256Hash.from_bytes(data)
        print(f'{sha256_1=}')

        hexed = hexlify(hashlib.sha256(data).digest())
        print(f'{hexed=}')

        def as_chunks(stream: BytesIO, chunk_size: int) -> Iterable[bytes]:
            while len(chunk := stream.read(chunk_size)) > 0:
                yield chunk

        

        # digest = hashlib.sha256(data).digest()
        # print(f'{digest=}')

        # mh = multihash.encode(digest, 'sha2-256')
        # print(f'{mh=}')

        # mh_h = multicodec.add_prefix('raw', mh)
        # print(f'{mh_h=}')

        # wrapped_digest = cid_sha256_hash_chunked(as_chunks(BytesIO(dumps(data)), 4))
        # print(f'{wrapped_digest=}')

        buffer1 = BytesIO(data)
        print(f'{buffer1=}')

        digest_leaves: list = []
        for chunk in as_chunks(buffer1, 4):
            print(chunk)
            digest_leaves.append((SHA256Hash.from_bytes_to_bytes(chunk)))

        # leaves: Leaves = Leaves(tuple(digest_leaves))

        print(f'{digest_leaves=}')

        mt = MerkleTree(tuple(digest_leaves, ))
        print(f'{mt=}')

        mt_root = mt.root()
        print(f'{mt_root=}')

        mh = multihash.from_hex_string(mt_root)

        # mt_root_digest = hashlib.sha256(str(mt_root).encode('utf-8')).hexdigest()
        # print(f'{mt_root_digest=}')

        # print(f'{digest_leaves=}')

        # mt_root_digest = hashlib.sha256(str(mt_root).encode('utf-8')).hexdigest()
        # print(f'{mt_root_digest=}')

        # digest = cid_sha256_hash_chunked(digest_leaves)
        # print(f'{digest=}')

        # mh = multihash.
        # print(f'{mh=}')
        # print(f'{mh=}')
        # mh_b58 = base58.b58encode(mt_root).decode('utf-8')
        # print(f'{mh_b58=}')
        # # multibase_prefix = multibase.encode('base58btc', wrapped_digest)
        # # print(f'{multibase_prefix=}')

        # cid0 = cid.CIDv0(mh_b58)
        # print(f'{cid0=}')
        # # print(f'{cid0.encode()}')

        # cid1 = cid.CIDv1('dag-pb', mh)
        # print(f'{cid1=}')

        # print(cid1.to_v0().encode())

        # ipfs_cid = base58.b58encode(cid0.to_v0().buffer).decode('utf-8')
        # print(f'{ipfs_cid=}')

        # # get the digest
        # digest = cid_sha256_hash_chunked(as_chunks(BytesIO(data), 4))
        # print(f'{digest=}')

        # # get the multihash
        # mh = multihash.encode(digest, 'sha2-256')
        # print(f'{mh=}')

        # cid = CIDv1('dag-pb', digest)
        # print(f'{cid=}')

        # get the multicodec
        # mc = multicodec.add_prefix('sha2-256', mh)
        # print(f'{mc=}')

        # # get the CID
        # cid = CIDv0(make_cid(0, 'dag-pb', mh))
        # print(f'{cid=}')

        # # get the base58 encoded CID
        # ipfs_cid = base58.b58encode(cid.buffer).decode('utf-8')

        # return ipfs_cid

        # # Compute the SHA-256 hash of the data
        # sha256_hash = hashlib.sha256(data).digest()
        # print(f'{sha256_hash=}')

        # # Create a multihash
        # mh = multihash.encode(sha256_hash, "sha2-256", 32)
        # print(f'{mh=}')

        # # Create a CID
        # cid = CIDv0(make_cid(0.0, 'dag-pb', mh))
        # print(f'{cid=}')

        # # Convert the CID to a base58 string
        # ipfs_cid = base58.b58encode(cid.buffer).decode('utf-8')

        # # return ipfs_cid
        # return ipfs_cid


        # # Compute the SHA-256 hash of the data
        # sha256_hash = hashlib.sha256(data).digest()
        # print(f'{sha256_hash=}')


        # # Create a multihash
        # mh = multihash.encode(sha256_hash, "sha2-256", 32)
        # print(f'{mh=}')

        # # Create a CID
        # cid = CIDv0(make_cid(0, 'dag-pb', mh))
        # print(f'{cid=}')

        # # Convert the CID to a base58 string
        # ipfs_cid = base58.b58encode(cid.buffer).decode('utf-8')
        # print(f'{ipfs_cid=}')

        # return ipfs_cid

        # mc = multicodec.add_prefix('sha2-256', mh)
        # print(f'{mc=}')

        # mc_cid = multicodec.add_prefix('dag-pb', mh)

        # print(f'{mc_cid=}')

        
        # multicodec_content_type = 0x70
        # multicodec_content_type_bytes = varint.encode(multicodec_content_type)
        # multihash_bytes = multicodec_content_type_bytes + mh

        # Encode the CID as a base58btc string
        # cid = base58.b58encode(mc_cid).decode('utf-8')

        # Create a multihash from the SHA-256 hash
        # multihash_bytes = multihash.encode(sha256_hash, 'sha2-256')

        # Prepend the codec code for 'dag-pb'
        # codec_bytes = varint.encode(0x70)
        # multicodec_bytes = multicodec.add_prefix('dag-pb', multihash_bytes)
        # cid_bytes = codec_bytes + multihash_bytes

        # Encode the CID as a base58btc string
        # cid = base58.b58encode(multicodec_bytes).decode('utf-8')

        # return cid
        # hash = hashlib.sha256(data).digest()
        # # multi_hash = multihash.encode(hash, 'sha2-256', 32)
        # multi_hash = multihash.encode(hash, 'sha2-256')
        # # multi_codec = multicodec.add_prefix(multi_hash, 'sha2-256')
        # cid_bytes = multicodec.add_prefix(0x70, multi_hash)
        # # cid_prefix = b'\x12\x20'
        # # multihash_bytes = cid_prefix + multi_hash
        # # cid_bytes = b'\x01\x70' + multihash_bytes
        # # return base58.b58encode(multi_hash).decode('utf-8')
        # return base58.b58encode(cid_bytes).decode('utf-8')

    # @staticmethod
    # def compute_ipfs_cid(data: bytes):
    #     # Compute the SHA-256 hash of the data
    #     sha256_hash = hashlib.sha256(data).digest()

    #     # c = cid_sha256_wrap_digest(sha256_hash)
    #     # Create a multihash
    #     mh = multihash.encode(sha256_hash, 0x12)

        # Create a CID
        # c = cid.make_cid(cid.V0, 'dag-pb', mh)
        # c = cid.make_cid(0, 'dag-pb', mh)
        # print(c)

        # # Convert the CID to a base58 string
        # print(c.to_v1().multihash)
        # ipfs_cid = base58.b58decode(c.buffer.decode('utf-8'))
        # ipfs_cid = c.buffer.decode('utf-8')

        # return ipfs_cid

    # def calculate_cid(self, data: bytes):
    #     sha256: str = hashlib.sha256(data).digest()
    #     print(f'{sha256=}')

        # mh = multihash.encode(sha256, 'sha2-256')

        # cid = ipfs_cid.cid_sha256_unwrap_digest(mh.decode('utf-8'))
        # # cid = ipfs_cid.cid_sha256_wrap_digest(sha256)
        # print(f'{cid=}')
        # # with self.psuedo_connect_client() as c:
        # #     return c.add_bytes(data)['Hash']
        # return cid

