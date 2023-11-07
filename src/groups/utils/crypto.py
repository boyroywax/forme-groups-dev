import hashlib
import re
from attrs import define, field, validators, Factory
from typing import NamedTuple, Tuple, override
# from ..base.types import BaseValueType


@define(frozen=True, slots=True, weakref_slot=False)
class SHA256Hash(str):
    """A SHA256 Hash object.
    """

    @override
    def __init__(self, data: str | bytes) -> None:
        # if not SHA256Hash.is_valid(data):
        #     raise ValueError(f"{data} is not a valid SHA256 hash")
        super().__init__()
        self = data

    @override
    def __str__(self) -> str:
        return f"{super().__str__()}"
    
    @override
    def __repr__(self) -> str:
        return f"{super().__str__()}"
        
    @classmethod
    def from_str(cls, data: str) -> str:
        return cls(SHA256Hash.hash(data.encode()))
    
    @classmethod
    def from_bytes(cls, data: bytes) -> str:
        return cls(SHA256Hash.hash(data))
    
    @classmethod
    def from_hex(cls, data: str) -> str:
        return cls(SHA256Hash.hash(bytes.fromhex(data)))
    
    @classmethod
    def from_str_to_bytes(cls, data: str) -> bytes:
        if isinstance(data, str):
            return cls(SHA256Hash.hash_bytes(data.encode()))
        # return cls(SHA256Hash.hash_bytes(data))
    
    @classmethod
    def from_bytes_to_bytes(cls, data: bytes) -> bytes:
        return cls(SHA256Hash.hash_bytes(data))
    
    @classmethod
    def from_hex_to_bytes(cls, data: str) -> bytes:
        return cls(SHA256Hash.hash_bytes(bytes.fromhex(data)))

    @staticmethod
    def hash(data: bytes) -> str:
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


class Leaves(Tuple):
    """A Leaves object.
    """

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
        if not isinstance(value, Tuple):
            return False
        if len(value) == 0:
            return False
        for item in value:
            if not isinstance(item, (SHA256Hash, str, bytes)):
                return False
        return True


@define(slots=True)
class MerkleTree:
    """A Merkle Tree object.
    """

    # leaves: tuple[str, ...] = field(
    #     default=Factory(Tuple),
    #     validator=validators.deep_iterable(validators.instance_of(str),
    #     iterable_validator=validators.instance_of(Tuple)))

    leaves: Leaves = field(
        default=Factory(Leaves),
        validator=validators.instance_of((Leaves, Tuple)))
    
    levels: tuple[tuple[str | bytes, ...]] = field(
        default=Factory(Tuple),
        validator=validators.deep_iterable(validators.deep_iterable(validators.instance_of((str, bytes)),
        iterable_validator=validators.instance_of(Tuple)),
        iterable_validator=validators.instance_of(Tuple)))

    def __init__(self, hashed_data: Tuple[str, ...] | Tuple[bytes, ...] | Leaves = (), use_all_bytes: bool = True) -> None:
        self.leaves = hashed_data
        self.levels = (self.leaves, )
        self.build()

    def build(self) -> None:
        level = self.leaves

        if len(self.levels[0]) == 1:
            self.levels = self.levels + ((self._hash_items(level[0]), ), )

        while len(level) > 1:
            hashed_level = self.hash_level(level)
            self.levels = self.levels + (hashed_level, )

            level = self.levels[-1]

    @staticmethod
    def _hash_func(data: str | bytes) -> str | bytes:
        if isinstance(data, str):
            return SHA256Hash.from_str_to_bytes(data)
        
        if isinstance(data, bytes):
            return SHA256Hash.from_bytes_to_bytes(data)
        
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
    
    def root(self) -> str | bytes | None:
        if self.levels[-1] is None or len(self.levels) == 0 or len(self.leaves) == 0:
            return None
        return self.levels[-1][0]

    def verify(self, leaf_hash: str | bytes) -> bool:
        if leaf_hash not in self.leaves:
            return False
        else:
            return True

    def __str__(self) -> str:
        return f"{self.root().decode()}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(root={self.root()})"
