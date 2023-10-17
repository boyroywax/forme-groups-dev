"""
The Schema declares the structure of the Group Unit Data.


"""

from attrs import define, field, validators
from typing import Any, TypeAlias, override, Type

from .interface import BaseInterface
from .types import BaseValueTypes, BaseContainerTypes, AllBaseValueTypes, AllBaseContainerTypes
from .container import BaseContainer
from .value import BaseValue
from ..utils.crypto import MerkleTree
from ..utils.converters import _base_type_converter


@define(frozen=True, slots=True, weakref_slot=False)
class SchemaEntry(BaseInterface):
    _key: str = field(validator=validators.instance_of(str))
    _value: str | type | TypeAlias = field(validator=validators.instance_of(str | type | TypeAlias), converter=_base_type_converter)


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
        return MerkleTree._hash_func(self._key)

    def _hash_value(self) -> str:
        return MerkleTree._hash_func(self._str_value(self._value))

    def _hash(self) -> MerkleTree:    
        return MerkleTree((self._hash_key(), self._hash_value()))
    
    def _verify_hash_key(self, key: str) -> bool:
        key_hash = MerkleTree._hash_func(key)
        return key_hash == self._hash_key()
    
    def _verify_hash_value(self, value: str | type | TypeAlias) -> bool:
        value_hash = MerkleTree._hash_func(self._str_value(value))
        return value_hash == self._hash_value()
    




@define(frozen=True, slots=True, weakref_slot=False)
class BaseSchema(BaseInterface):
    _entries: tuple[SchemaEntry, ...] = field(
        validator=validators.deep_iterable(validators.instance_of(SchemaEntry), iterable_validator=validators.instance_of(tuple)),
    )

    @property
    def entries(self) -> tuple[SchemaEntry, ...]:
        """The entries held by the BaseSchema Class

        Returns:
            tuple[SchemaEntry]: The entries held by the BaseSchema Class

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
        for entry in self.entries:
           yield entry

    @override
    def __repr__(self):
        return f"{self.__class__.__name__}(entries={repr(entry for entry in self.entries)})"
    
    def _hash_entries(self):
        hashed_entries: tuple[str, ...] = ()
        for entry in self.entries:
            hashed_entries.append(entry._hash.root())
            
        return MerkleTree(hashed_data=hashed_entries)
