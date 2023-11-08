import hashlib
from attrs import define, field, validators, Factory, converters
from typing import Any, Iterable, NamedTuple, Tuple, override, Optional


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
    raise ValueError(f"Expected data to be str, got {type(data)}")

@define(frozen=True, slots=True, weakref_slot=False)
class SHA256Hash:
    """A SHA256 Hash object.
    """

    raw_hash: bytes = field(
        default=Factory(bytes),
        converter=convert_str_to_bytes,
        validator=validators.instance_of(bytes))
    
    @property
    def hash(self) -> bytes:
        return self.raw_hash

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
        
        raise ValueError(f"Expected data to be str or bytes, got {type(data)}")
    
    @override
    def __str__(self) -> str:
        return f"{self.hash.decode("ascii")}"
    
    @override
    def __repr__(self) -> str:
        return f"{str(self.hash.decode("ascii"))}"
        
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

    # @staticmethod
    # def raw_hash(data: bytes) -> str:
    #     """Hashes a string using SHA256

    #     Args:
    #         data (str): The string to hash
        
    #     Returns:
    #         str: The hashed string
    #     """
    #     return hashlib.sha256(data).hexdigest()
    
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
            return self.raw_hash == other.encode()
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