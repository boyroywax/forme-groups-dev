import hashlib
from attrs import define, field, validators, Factory, converters
from typing import Any, Iterable, NamedTuple, Tuple, override, Optional
from .sha256 import SHA256Hash
# from ..base.types import BaseValueType


def _convert_hash(value: str | bytes | SHA256Hash) -> SHA256Hash:
    if isinstance(value, str):
        return SHA256Hash.from_str(value)
    if isinstance(value, bytes):
        return SHA256Hash.from_bytes(value)
    if isinstance(value, SHA256Hash):
        return value
    raise ValueError(f"Expected hash to be str or bytes or SHA256Hash, got {type(value)}")


@define(frozen=True, slots=True, weakref_slot=False)
class Leaf:
    """A Leaf object.
    """
    hash: SHA256Hash = field(
        converter=_convert_hash,
        default=Factory(SHA256Hash))

    @hash.validator
    def _check_hash(self, attribute, value):
        if not isinstance(value, SHA256Hash):
            raise ValueError(f"Expected hash to be SHA256Hash, got {type(value)}")


def convert_to_SHA256Hash(data: Tuple[str | bytes | SHA256Hash, ...]) -> Tuple['SHA256Hash', ...]:
    """Converts a string to bytes

    Args:
        data (str): The string to convert

    Returns:
        bytes: The converted string
    """
    sha256_objects: Tuple['SHA256Hash', ...] = ()
    for item in data:
        if not isinstance(item, (str, bytes, SHA256Hash)):
            raise ValueError(f"Expected data to be str or bytes, got {type(item)}")
        if isinstance(item, str):
            sha256_objects = sha256_objects + tuple([SHA256Hash.from_str(item)])
        if isinstance(item, bytes):
            sha256_objects += tuple([SHA256Hash.from_bytes(item)])
        if isinstance(item, SHA256Hash):
            sha256_objects += tuple(item, )

        print(f'{sha256_objects=}')
        # raise ValueError(f"Expected data to be str or bytes or SHA256Hash, got {type(data)}")
    return sha256_objects

@define(frozen=True, slots=True)
class Leaves:
    """A Leaves object.
    """

    leaves: Tuple[SHA256Hash, ...] = field(
        default=tuple(),
        converter=convert_to_SHA256Hash,
        validator=validators.deep_iterable(validators.instance_of((SHA256Hash)),
        iterable_validator=validators.instance_of(tuple)))
    


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
    
    def __len__(self) -> int:
        return len(self.leaves)
    
    def __iter__(self) -> Iterable[SHA256Hash]:
        for leaf in self.leaves:
            yield leaf


def convert_loose_leaves_to_levels(data: Tuple[SHA256Hash, ...] | Tuple[str, ...] | Tuple[bytes, ...]) -> Leaves:
    leaf_hashes: list[SHA256Hash] = []
    if isinstance(data, tuple):
        if len(data) == 0:
            return None
        for item in data:
            if not isinstance(item, (SHA256Hash, str, bytes)):
                raise ValueError(f"Expected data to be str or bytes, got {type(item)}")
            if isinstance(item, str):
                leaf_hashes.append(SHA256Hash.from_str(item))
            if isinstance(item, bytes):
                leaf_hashes.append(SHA256Hash.from_bytes(item))
            if isinstance(item, SHA256Hash):
                leaf_hashes.append(item)
            
        return Leaves(tuple(leaf_hashes))


@define(slots=True)
class MerkleTree:
    """A Merkle Tree object.
    """

    # leaves: tuple[str, ...] = field(
    #     default=Factory(Tuple),
    #     validator=validators.deep_iterable(validators.instance_of(str),
    #     iterable_validator=validators.instance_of(Tuple)))

    leaves: Optional[Leaves] = field(
        default=None,
        converter=convert_loose_leaves_to_levels,
        validator=validators.optional(validators.instance_of(Leaves)))
    
    levels: Optional[Tuple[Leaves, ...]] = field(default=tuple())
        # validator=validators.deep_iterable(validators.instance_of(Leaves | tuple),
        # iterable_validator=validators.instance_of(tuple)))

    def __init__(self, hashed_data: Tuple[SHA256Hash, ...] | Tuple[str, ...] | Tuple[bytes, ...] | Leaves = (), use_all_bytes: bool = True) -> None:
        self.leaves = hashed_data if isinstance(hashed_data, Leaves) else convert_loose_leaves_to_levels(hashed_data)
        _levels = (self.leaves, )
        # self.levels = convert_loose_leaves_to_levels(_levels)
        self.levels = _levels
        self.build()

    def build(self) -> None:
        level = (self.leaves, )

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
    def _hash_items(item1: bytes | None = None, item2: bytes | None = None) -> bytes:
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
    def root(self) -> str:
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
