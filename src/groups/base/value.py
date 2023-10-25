import struct
from functools import lru_cache
from typing import override, Any, Union
from attrs import define, field


from .types import BaseValueTypes, BaseValueTypes
from .interface import BaseInterface
from .exceptions import GroupBaseValueException
from ..utils.crypto import MerkleTree
from ..utils.converters import force_value_type


def _base_value_validator(instance, attribute, value):
    """Validates the argument is a BaseValueTypes

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        GroupBaseValueException: If the value is not a BaseValueTypes
    """
    if not isinstance(value, BaseValueTypes):
        raise GroupBaseValueException(f"Expected a value, but received {type(value)}")


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValue(BaseInterface):
    """Base class for values

    Args:
        value (BaseValueTypes): The value to hold

    Raises:
        GroupBaseValueException: If the value is not a BaseValueType

    Examples:
        >>> value = BaseValue(1)
        >>> value
        BaseValue(value=1, type=int)
    """
    _value: BaseValueTypes = field(validator=_base_value_validator)

    @property
    def value(self) -> BaseValueTypes:
        """The single base value held by the BaseValue Class

        Returns:
            BaseValueTypes: The value held by the BaseValue Class

        Examples:
            >>> value = BaseValue(1)
            >>> value.value
            1
        """
        return self._value
    
    @value.getter
    def value(self) -> BaseValueTypes:
        """The single base value held by the BaseValue Class
        """
        return self._value

    @staticmethod
    def _peek_value(value: 'BaseValue') -> BaseValueTypes:
        """Peeks the value of a BaseValue

        Args:
            value (BaseValue): The value to peek

        Returns:
            unit_value_types: The value of the BaseValue

        Raises:
            GroupBaseValueException: If the value is not a BaseValue
        """
        if isinstance(value, BaseValue):
            return value.value

        raise GroupBaseValueException(f"Expected a BaseValue, but received {type(value)}")
    
    @staticmethod
    def _force_type(
        value: Union["BaseValue", BaseValueTypes],
        type_alias: str
    ) -> 'BaseValue':
        """Forces a value to a type

        Args:
            value (unit_value_types): The value to force
            type_ (unit_types): The type to force the value to

        Returns:
            unit_value_types: The forced value

        Raises:
            TypeError: If the value could not be forced to the type

        Examples:
            >>> value = BaseValue("1")
            >>> forced_value = value._force_type(value, "int")
            >>> forced_value
            BaseValue(value=1, type=int)
        """
        if isinstance(value, BaseValue):
            value = value.value

        if value is None:
            return BaseValue(None)
        
        assert isinstance(value, BaseValueTypes), f"Expected a value, but received {type(value)}"

        forced_value: Any = force_value_type(value, type_alias)

        return BaseValue(forced_value)

    def get_type_str(self) -> str:
        """Returns the type of the value as a string

        Returns:
            str: The type of the value

        Examples:
            >>> value = BaseValue(1)
            >>> value.get_type_str()
            'int'
        """
        return type(self._value).__name__

    @override
    def __str__(self) -> str:
        """The String of the value of the BaseValue

        Returns:
            str: The String of the value of the BaseValue

        Examples:
            >>> value = BaseValue(1)
            >>> str(value)
            '1'
        """
        return str(self._value)

    @override
    def __repr__(self) -> str:
        """The full String representation of the BaseValue

            Returns:
                str: The full String representation of the BaseValue, including the value and type.

            Examples:
                >>> value = BaseValue(1)
                >>> repr(value)
                BaseValue(value=1, type=int)
        """
        return f"{self.__class__.__name__}(value={repr(self.value)}, type={self.get_type_str()})"

    # @lru_cache(maxsize=1)
    def _hash_value(self) -> str:
        """Hashes the repr(value) of the BaseValue

            Returns:
                str: The hashed value

            Examples:
                >>> value = BaseValue(1)
                >>> value._hash_value()
                '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b'
        """
        return MerkleTree._hash_func(repr(self.value))

    # @lru_cache(maxsize=1)
    def _hash_type(self) -> str:
        """Hashes the type of the BaseValue

            Returns:
                str: The hashed type

            Examples:
                >>> value = BaseValue(1)
                >>> value._hash_type()
                '6da88c34ba124c41f977db66a4fc5c1a951708d285c81bb0d47c3206f4c27ca8'
        """
        return MerkleTree._hash_func(self.get_type_str())

    # @lru_cache(maxsize=1)
    def _hash(self) -> MerkleTree:
        """Hashes the BaseValue by hashing the value and type separatly

            Returns:
                MerkleTree: The hashed BaseValue

            Examples:
                >>> value = BaseValue(1)
                >>> value._hash()
                MerkleTree(root='5b1980a185761ca08c85b7ae8d9d98176814e6161f86df9bbc0b5ae4311ba46a')
        """
        return MerkleTree(hashed_data=(self._hash_value(), self._hash_type(), ))

    def _verify_hash_value(self, hash_value: str) -> bool:
        """Verifies the hash value of the BaseValue

            Args:
                hash_value (str): The hash value to verify

            Returns:
                bool: Whether the hash value is valid

            Examples:
                >>> value = BaseValue(1)
                >>> value._verify_hash_value('6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b')
                True
        """
        return self._hash_value() == hash_value

    def _verify_hash_type(self, hash_type: str) -> bool:
        """Verifies the hash type of the BaseValue

            Args:
                hash_type (str): The hash type to verify

            Returns:
                bool: Whether the hash type is valid

            Examples:
                >>> value = BaseValue(1)
                >>> value._verify_hash_type('6da88c34ba124c41f977db66a4fc5c1a951708d285c81bb0d47c3206f4c27ca8')
                True
        """
        return self._hash_type() == hash_type

    def _verify_hash(self, hash_: str) -> bool:
        """Verifies the hash of the BaseValue

            Args:
                hash_ (str): The hash to verify

            Returns:
                bool: Whether the hash is valid

            Examples:
                >>> value = BaseValue(1)
                >>> value._verify_hash('5b1980a185761ca08c85b7ae8d9d98176814e6161f86df9bbc0b5ae4311ba46a')
                True
        """
        return self._hash().root() == hash_
    
    def _to_dict(self):
        return {
            "value": self.value,
            "type": self.get_type_str()
        }
    
    @classmethod
    def _from_dict(cls, data: dict) -> 'BaseValue':
        return BaseValue._force_type(data["value"], data["type"])
