"""
The Schema declares the structure of the Group Unit Data.


"""

from attrs import define, field, validators
from typing import TypeAlias, override, Tuple

from .interface import BaseInterface
from .types import BaseTypes, BaseContainerTypes
from ..utils.crypto import MerkleTree


def _validate_schema_entry_key(instance, attribute, value):
    """Validates the argument is a str

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        TypeError: If the value is not a str
    """
    if not isinstance(value, str):
        raise TypeError(f"Expected a str, but received {type(value)}")

    split_key: Tuple[str, ...] = value.split(' ')
    if len(split_key) > 1:
        raise TypeError(f"Expected a str without spaces, but received {value}")
    
    if len(split_key) == 1 and len(split_key[0]) == 0:
        raise TypeError(f"Expected a str without spaces, but received {value}")
    
    if len(split_key) == 1 and len(split_key[0]) > 0:
        if split_key[0] == '':
            raise TypeError(f"Expected a non empty str, but received {value}")

        if len(split_key[0]) > 256:
            raise TypeError(f"Expected a str with length 256 or less, but received len={len(split_key[0])}, value={value}")
        return split_key[0]
    

def _base_type_converter(item: str | type) -> TypeAlias | type:
    """
    Converter function for _value field
    """
    type_from_alias: TypeAlias | type = None
    
    if isinstance(item, str) and len(item) > 0:
        type_from_value_alias = BaseTypes._get_type_from_alias(item)
        type_from_container_alias = BaseTypes._get_type_from_alias(item)

        assert (type_from_value_alias is not None or
                type_from_container_alias is not None), f"Expected a type, but received {item}"
        type_from_alias = type_from_value_alias if type_from_value_alias is not None else type_from_container_alias

    elif isinstance(item, type):
        type_from_alias = item

    elif isinstance(item, BaseContainerTypes):
        type_from_alias = item.__class__

    return type_from_alias


@define(frozen=True, slots=True, weakref_slot=False)
class SchemaEntry(BaseInterface):
    """The SchemaEntry class holds the key-value pair of the schema

    Args:
        key (str): The key of the key-value pair
        value (str | type | TypeAlias): The value of the key-value pair

    Examples:
        >>> entry = SchemaEntry(key='name', value=str)

    Raises:
        TypeError: If value is not a str, type or TypeAlias
    """
    _key: str = field(validator=_validate_schema_entry_key)

    _value: str | type | TypeAlias = field(
        validator=validators.instance_of((str, type)),
        converter=_base_type_converter)

    @staticmethod
    def _str_value(value: str | type | TypeAlias) -> str:
        return value.__name__ if isinstance(value, type) else value

    @override
    def __str__(self):
        return f"key={self._key}, value={self._str_value(self._value)}"

    @override
    def __repr__(self):
        return f"{self.__class__.__name__}(key={repr(self._key)}, value={self._str_value(self._value)})"

    def _hash_key(self) -> str:
        """Hashes the key of the key-value pair

        Returns:
            str: The hashed key
        """
        return MerkleTree._hash_func(self._key)

    def _hash_value(self) -> str:
        """Hashes the value of the key-value pair

        Returns:
            str: The hashed value
        """
        return MerkleTree._hash_func(self._str_value(self._value))

    def _hash(self) -> MerkleTree:
        """Hashes the key-value pair as leaves of a MerkleTree

        Returns:
            MerkleTree: The hashed key-value pair
        """ 
        return MerkleTree((self._hash_key(), self._hash_value()))

    def _verify_hash_key(self, key: str) -> bool:
        """Verifies the key of the key-value pair

        Args:
            key (str): The key to verify

        Returns:
            bool: True if the key is verified, False otherwise
        """
        key_hash = MerkleTree._hash_func(key)
        return key_hash == self._hash_key()

    def _verify_hash_value(self, value: str | type | TypeAlias) -> bool:
        """Verifies the value of the key-value pair

        Args:
            value (str | type | TypeAlias): The value to verify

        Returns:
            bool: True if the value is verified, False otherwise
        """
        value_hash = MerkleTree._hash_func(self._str_value(value))
        return value_hash == self._hash_value()
    

def _key_is_duplicate(key: str, entries: Tuple[SchemaEntry, ...]) -> bool:
    """Checks if the key is in the entries

    Args:
        key (str): The key to check
        entries (Tuple[SchemaEntry, ...]): The entries to check

    Returns:
        bool: True if the key is in the entries, False otherwise
    """
    single_instance: bool = True
    instance_count: int = 0

    for entry in entries:
        if entry._key == key:
            instance_count += 1
            if instance_count > 1:
                single_instance = False
                break
    return not single_instance

def _validate_schema_entries(instance, attribute, value):
    """Validates the argument is a Tuple of SchemaEntry

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        TypeError: If the value is not a Tuple of SchemaEntry
    """
    if not isinstance(value, Tuple):
        raise TypeError(f"Expected a Tuple, but received {type(value)}")

    for item in value:
        if not isinstance(item, SchemaEntry):
            raise TypeError(f"Expected a Tuple of SchemaEntry, but received {type(value)}")
        if _key_is_duplicate(item._key, value):
            raise TypeError(f"Expected a Tuple of SchemaEntry with unique keys, but received {value}")
        # if len(item._key) == 0:
        #     raise TypeError(f"Expected a Tuple of SchemaEntry with non-empty keys, but received {value}")
        # if len(item._key) > 256:
        #     raise TypeError(f"Expected a Tuple of SchemaEntry with keys of length 256 or less, but received {value}m len={len(item._key)}")



@define(frozen=True, slots=True, weakref_slot=False)
class BaseSchema(BaseInterface):
    """The Schema declares the structure of group data.

    Args:
        entries (Tuple[SchemaEntry, ...]): The entries held by the BaseSchema Class

    Examples:
        >>> schema = BaseSchema((SchemaEntry(key='name', value=str), SchemaEntry(key='age', value=int)))

    Raises:
        TypeError: If entries is not a Tuple of SchemaEntry
    """
    _entries: Tuple[SchemaEntry, ...] = field(
        validator=_validate_schema_entries)

    @property
    def entries(self) -> Tuple[SchemaEntry, ...]:
        """The entries held by the BaseSchema Class

        Returns:
            Tuple[SchemaEntry]: The entries held by the BaseSchema Class

        Examples:
            >>> schema = BaseSchema((SchemaEntry(key='name', value=str), SchemaEntry(key='age', value=int)))
            >>> schema.entries
            (SchemaEntry(key='name', value=str), SchemaEntry(key='age', value=int))
        """
        return self._entries
    
    def get_entry(self, key: str) -> SchemaEntry:
        """Gets the entry with the given key

        Args:
            key (str): The key of the entry

        Returns:
            SchemaEntry: The entry with the given key

        Examples:
            >>> schema = BaseSchema((SchemaEntry(key='name', value=str), SchemaEntry(key='age', value=int)))
            >>> schema.get_entry('name')
            SchemaEntry(key='name', value=str)
        """
        for entry in self.entries:
            if entry._key == key:
                return entry
        raise KeyError(f"Key {key} not found in schema")
    
    @override
    def __iter__(self):
        """Iterates over the entries in the schema

        Yields:
            SchemaEntry: The entries in the schema
        
        Examples:
            >>> schema = BaseSchema((SchemaEntry(key='name', value=str), SchemaEntry(key='age', value=int)))
            >>> for entry in schema:
            ...     print(entry)
            key='name', value=str
            key='age', value=int
        """
        for entry in self.entries:
            yield entry

    @override
    def __str__(self):
        """Returns the string representation schema's entries
        
        Returns:
            str: The string representation of the schema's entries
        """
        return f"({'), ('.join(str(entry) for entry in self.entries)})"

    @override
    def __repr__(self):
        """Returns the representation of the schema

        Returns:
            str: The representation of the schema
        """
        return f"{self.__class__.__name__}(entries={repr(self.entries)})"
    
    def _hash_entries(self):
        """Hashes the entries of the schema
        
        Returns:
            MerkleTree: The hashed entries of the schema

        Examples:
            >>> schema = BaseSchema((SchemaEntry(key='name', value=str), SchemaEntry(key='age', value=int)))
            >>> schema._hash_entries()
            MerkleTree(hashed_data=('fbc595a11273e6f79f13f9210d7d60660c8ad127aa6b870b841c4b2a8ff75cb2', '5422c43fc239d7228d8aca8f9310bca3ce00cea3256adb0db595a2b1c211a7e4'))
        """
        hashed_entries: Tuple[str, ...] = ()
        for entry in self.entries:
            hashed_entries += (entry._hash().root(), )
            
        return MerkleTree(hashed_data=hashed_entries)
