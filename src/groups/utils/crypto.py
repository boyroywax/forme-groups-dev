
import hashlib
import re
from attrs import define, field, validators, Factory, converters
from typing import Any, Iterable, NamedTuple, Tuple, override, Optional
# from ..base.types import BaseValueType

def convert_bytes_to_str(data: bytes) -> str:
    if isinstance(data, bytes):
        return data.decode()
    return data

@define(frozen=True, slots=False)
class SHA256Hash(bytes):
    """A SHA256 Hash object.
    """

    # @override
    # def __init__(self, data: str | bytes) -> None:
    #     # if not SHA256Hash.is_valid(data):
    #     #     raise ValueError(f"{data} is not a valid SHA256 hash")
    #     # super().__init__()
    #     self = data
    # raw_hash: bytes = field(
    #     default=Factory(bytes),
    #     validator=validators.instance_of(bytes))
    
    raw_hash: bytes = field(
        default=bytes())
        # converter=convert_bytes_to_str)
        # validator=validators.instance_of((str, bytes)))
    
    # @_hash_to_hex_digest.
    # def _convert_hash_to_hex_digest(self, value: str | bytes) -> str:
    #     if isinstance(value, bytes):
    #         return value.hex()
    #     return value

    @classmethod
    def hash_sha256(cls, data: bytes) -> 'SHA256Hash':
        """Hashes a string using SHA256

        Args:
            data (str): The string to hash
        
        Returns:
            str: The hashed string
        """
        if isinstance(data, bytes):
            return SHA256Hash(hashlib.sha256(data).digest())
        
        raise ValueError(f"Expected data to be str or bytes, got {type(data)}")
    
    @property
    def hash(self) -> bytes:
        if self.raw_hash is None:
            raise ValueError("self._hash is None")
        if isinstance(self.raw_hash, str):
            return self.raw_hash.encode()
        if isinstance(self.raw_hash, bytes):
            return self.raw_hash
        raise ValueError(f"Expected self._hash to be str or bytes, got {type(self.raw_hash)}")

    # @override
    # def __str__(self) -> str:
    #     return f"{super().__str__()}"
    
    # @override
    # def __repr__(self) -> str:
    #     return f"{super().__str__()}"

    # def hex(self) -> str:
    #     return self.hash.hex()

    @override
    def __str__(self) -> str:
        return f"{self.hash.decode('ascii')}"
    
    @override
    def __repr__(self) -> str:
        return f"{str(self.hash)}"
        
    @classmethod
    def from_str(cls, data: str) -> 'SHA256Hash':
        return SHA256Hash.hash_sha256(data.encode())
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'SHA256Hash':
        return SHA256Hash.hash_sha256(data)
    
    @classmethod
    def from_hex(cls, data: str) -> 'SHA256Hash':
        return SHA256Hash.hash_sha256(bytes.fromhex(data))
    
    @classmethod
    def from_str_to_bytes(cls, data: str) -> bytes:
        if isinstance(data, str):
            return SHA256Hash.hash_bytes(data.encode())
        # return cls(SHA256Hash.hash_bytes(data))
    
    @classmethod
    def from_bytes_to_bytes(cls, data: bytes) -> bytes:
        return SHA256Hash.hash_bytes(data)
    
    @classmethod
    def from_hex_to_bytes(cls, data: str) -> bytes:
        return SHA256Hash.hash_bytes(bytes.fromhex(data))

    @staticmethod
    def raw_hash(data: bytes) -> str:
        """Hashes a string using SHA256

        Args:
            data (str): The string to hash
        
        Returns:
            str: The hashed string
        """
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def hash_bytes(data: bytes) -> bytes:
        """Hashes a string using SHA256

        Args:
            data (bytes): The string to hash
        
        Returns:
            bytes: The hashed string
        """
        return hashlib.sha256(data).digest()

    @staticmethod
    def is_valid(value: str | bytes) -> bool:
        """Checks if a string is a valid SHA256 hash

        Args:
            value (str): The string to check

        Returns:
            bool: Whether the string is a valid SHA256 hash
        """
        # if isinstance(value, bytes):
        #     value = value.decode()

        if not isinstance(value, (str, bytes)):
            return False
        if len(value) != 64:
            return False
        if not re.match(r'^[0-9a-fA-F]+$', value):
            return False
        return True
    
    @override
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SHA256Hash):
            return self.raw_hash == other.raw_hash
        if isinstance(other, str):
            return self.hash == other
        if isinstance(other, bytes):
            return self.raw_hash == other
        return False
    
    @override
    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
    
    def __call__(self) -> str:
        return self.raw_hash
    
    def __add__(self, other: 'SHA256Hash') -> str:
        assert isinstance(other, SHA256Hash), f"{type(other)} must be SHA256Hash"
        return self.raw_hash + other.raw_hash


class Leaves(Tuple[Any, ...]):
    """A Leaves object.
    """

    # leaves: tuple[SHA256Hash, ...] | tuple[str, ...] | tuple[bytes, ...] = field(
    #     default=tuple)
        # validator=validators.deep_iterable(validators.instance_of((SHA256Hash, str, bytes)), 
        # iterable_validator=validators.instance_of(tuple)))

    def __init__(self, data: Tuple[SHA256Hash, ...] | Tuple[str, ...] | Tuple[bytes, ...]) -> None:
        if not Leaves.is_valid(data):
            raise ValueError(f"{data} is not a valid Leaves object")
        super().__init__()
        self = data

    @staticmethod
    def is_valid(value: Tuple[SHA256Hash, ...] | Tuple[str, ...] | Tuple[bytes, ...]) -> bool:
        """Checks if a tuple is a valid Leaves object

        Args:
            value (tuple[str, ...]): The tuple to check

        Returns:
            bool: Whether the tuple is a valid Leaves object
        """
        if not isinstance(value, tuple):
            return False
        if len(value) == 0:
            return False
        for item in value:
            if not isinstance(item, (SHA256Hash, str, bytes)):
                return False
        return True
    

def convert_loose_leaves_to_levels(data: Tuple[SHA256Hash, ...] | Tuple[str, ...] | Tuple[bytes, ...]) -> Tuple[Leaves, ...]:
    if isinstance(data, tuple):
        if len(data) == 0:
            return ()
        for item in data:
            if not isinstance(item, (SHA256Hash, str, bytes)):
                raise ValueError(f"Expected data to be str or bytes, got {type(item)}")
        return (Leaves(data), )
    return ()


@define(slots=True)
class MerkleTree:
    """A Merkle Tree object.
    """

    # leaves: tuple[str, ...] = field(
    #     default=Factory(Tuple),
    #     validator=validators.deep_iterable(validators.instance_of(str),
    #     iterable_validator=validators.instance_of(Tuple)))

    leaves: Tuple[SHA256Hash, ...] | Tuple[str, ...] | Tuple[bytes, ...] | Leaves = field()
        # default=Tuple[str, ...])
        # validator=validators.instance_of((Leaves, tuple)))
    
    levels: Optional[Tuple[Any, ...]] = field(default=tuple())
        # validator=validators.deep_iterable(validators.instance_of(Leaves | tuple),
        # iterable_validator=validators.instance_of(tuple)))

    def __init__(self, hashed_data: Tuple[SHA256Hash, ...] | Tuple[str, ...] | Tuple[bytes, ...] | Leaves = (), use_all_bytes: bool = True) -> None:
        self.leaves = hashed_data
        _levels = hashed_data
        self.levels = convert_loose_leaves_to_levels(_levels)
        self.build()

    def build(self) -> None:
        level = self.leaves

        if len(self.levels[0]) == 1:
            self.levels = self.levels + (self._hash_items(level[0]), )

        while len(level) > 1:
            hashed_level = self.hash_level(level)
            self.levels = self.levels + (hashed_level, )

            level = self.levels[-1]

    @staticmethod
    def _hash_func(data:  str | bytes | tuple | SHA256Hash) -> bytes:
        """Hashes a string using SHA256

        Args:
            data (str): The string to hash
        
        Returns:
            str: The hashed string
        """
        possible_multiple_data_items = MerkleTree._hash_func_iter(data)

        for item in possible_multiple_data_items:

            if isinstance(item, SHA256Hash):
                return item.hash

            if isinstance(item, str):
                return item
            
            if isinstance(item, bytes):
                return item
            
            raise ValueError(f"Expected data to be str or bytes, got {type(item)}")

        return hashlib.sha256(data).digest()


    @staticmethod
    def _hash_func_iter(data: str | bytes | tuple | SHA256Hash) -> Iterable[bytes]:
        if isinstance(data, str):
            yield SHA256Hash.from_str_to_bytes(data)
        
        if isinstance(data, bytes):
            yield SHA256Hash.from_bytes_to_bytes(data)
        
        if isinstance(data, tuple):
            for item in data:
                if isinstance(item, str):
                    yield SHA256Hash.from_str_to_bytes(item)
                
                if isinstance(item, bytes):
                    yield SHA256Hash.from_bytes_to_bytes(item)
                
                if isinstance(item, SHA256Hash):
                    yield item.hash
                
                raise ValueError(f"Expected data to be str or bytes, or SHA256Hash, got {type(item)}")
        
        raise ValueError(f"Expected data to be str or bytes, got {type(data)}")

    @staticmethod
    def _hash_items(item1: str | bytes | None = None, item2: str | bytes | None = None) -> str | bytes:
        # assert ((type(item1) is str) or (type(item2) is None)), f"{type(item2)} must be str or None"
        if item1 is None:
            raise ValueError(f'item1 cannot be None, but received {type(item1)})')

        if item2 is None:
            return MerkleTree._hash_items(item1, item1)

        return MerkleTree._hash_func(item1 + item2)

    @staticmethod
    def hash_level(level: tuple[str | bytes, ...]) -> tuple[str, ...]:
        hashed_level = ()
        for i in range(0, len(level), 2):
            if (i + 1) % 2 != 0 and i == len(level) - 1:
                hashed_level = hashed_level + (MerkleTree._hash_items(level[i]), )
            elif (i + 1 <= len(level) - 1):
                hashed_level = hashed_level + (MerkleTree._hash_items(level[i], level[i + 1]), )
            else:
                raise Exception("This should never happen")

        return hashed_level

    def _find_levels_count(self) -> int:
        return len(self.levels)
    
    @property
    def root(self) -> str | bytes | None | SHA256Hash:
        if self.levels[-1] is None or len(self.levels) == 0 or len(self.leaves) == 0:
            return None
        return self.levels[-1][0]

    def verify(self, leaf_hash: str | bytes) -> bool:
        if leaf_hash not in self.leaves:
            return False
        else:
            return True

    def __str__(self) -> str:
        return f"{self.root}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(root={self.root})"
