import hashlib
import re
from attrs import define, field, Factory
from typing import Any, Iterable, override


def convert_str_to_bytes(data: str | bytes) -> bytes:
    """Converts a string to bytes

    Args:
        data (str): The string to convert

    Returns:
        bytes: The converted string
    """
    if isinstance(data, str):
        return data.encode()
    if isinstance(data, bytes):
        return data
    raise ValueError(f"Expected data to be str or bytes, got {type(data)}")


@define(frozen=True, slots=True, weakref_slot=False)
class SHA256Hash:
    """A SHA256 Hash object.
    """

    _raw_hash: bytes | str = field(default=Factory(bytes))

    @_raw_hash.validator
    def _check_hash(self, attribute, value):
        if not isinstance(value, (str, bytes)):
            raise ValueError(f"Expected hash to be str or bytes, got {type(value)}")
        
        if value in [None, '', ' ', b'', b' ']:
            raise ValueError("Expected hash to be not None or empty string")
        
        if isinstance(value, str):
            value = value.encode()

        if len(value) != 32:
            raise ValueError("Expected hash to be 32 bytes")
        
        if not re.match(r'^[0-9a-fA-F]+$', value.hex()):
            raise ValueError("Expected hash to be hex")

    @property
    def hash(self) -> bytes:
        return convert_str_to_bytes(self._raw_hash)
    
    @property
    def string(self) -> str:
        return self.hash.decode()
    
    @property
    def hex(self) -> str:
        return self.hash.hex()

    @classmethod
    def hash_sha256(cls, data: bytes) -> 'SHA256Hash':
        """Hashes a string using SHA256

        Args:
            data (str): The string to hash
        
        Returns:
            str: The hashed string
        """
        if isinstance(data, bytes):
            return cls(hashlib.sha256(data).digest())
        
        raise ValueError(f"Expected data to be bytes, got {type(data)}")
    
    @override
    def __str__(self) -> str:
        return f"{self.hash.decode()}"
    
    @override
    def __repr__(self) -> str:
        return f"{str(self.hash.decode())}"
        
    @classmethod
    def from_str(cls, data: str) -> 'SHA256Hash':
        return cls.hash_sha256(data.encode())
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'SHA256Hash':
        return cls.hash_sha256(data)
    
    @classmethod
    def from_hex(cls, data: str) -> 'SHA256Hash':
        return cls.hash_sha256(bytes.fromhex(data))
    
    @classmethod
    def from_(cls, data: str | bytes | Any) -> 'SHA256Hash':
        if isinstance(data, str):
            return cls.from_str(data)
        if isinstance(data, bytes):
            return cls.from_bytes(data)
        if isinstance(data, int):
            return cls.from_hex(f"{data}")
        if isinstance(data, SHA256Hash):
            return data
        raise ValueError(f"Expected data to be str, bytes or SHA256Hash, got {type(data)}")
    
    @override
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SHA256Hash):
            return self.hash == other.hash
        if isinstance(other, str):
            return self.hash == other.encode()
        if isinstance(other, bytes):
            return self.hash == other
        return False
    
    @override
    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)
    
    def __call__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: 'SHA256Hash') -> bytes:
        assert isinstance(other, SHA256Hash), f"{type(other)} must be SHA256Hash"
        return self.hash + other.hash
    
    def __iter__(self) -> Iterable[bytes]:
        yield self.hash