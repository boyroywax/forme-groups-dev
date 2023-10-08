import struct
from attrs import define, field, validators
from typing import override, Any, Union


from .types import UnitValueTypes, UnitTypes, Number, Integer
from .interface import BaseInterface
from .exceptions import GroupBaseValueException
# from ..utils.converters import _convert_container_to_value
from ..utils.crypto import MerkleTree


def _base_value_validator(instance, attribute, value):
    if not isinstance(value, UnitValueTypes):
        raise GroupBaseValueException(f"Expected a value, but received {type(value)}")


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValue[T: UnitValueTypes](BaseInterface):
    """Base class for values
    """
    _value: T = field(validator=_base_value_validator)

    @property
    def value(self) -> T:
        return self._value

    @staticmethod
    def _peek_value(value: 'BaseValue') -> UnitValueTypes:
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
        value: Union["BaseValue", UnitValueTypes],
        type_: str
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
            if value.get_type_str() == type_:
                return value
            
            value = value.value

        assert isinstance(value, UnitValueTypes), f"Expected a value, but received {type(value)}"
        forced_value: Any = None

        base_exception: GroupBaseValueException = GroupBaseValueException(f"Could not force value {value} to type {type_}")

        try:
            match(type_):
                case "<class 'NoneType'>" | "NoneType" | "None":
                    return BaseValue(None)
                case "<class 'bool'>" | "bool" | "boolean":
                    forced_value = bool(value)
                case "<class 'int'>" | "int" | "integer":
                    forced_value = int(value)
                case "<class 'float'>" | "float":
                    forced_value = float(value)
                case "<class 'str'>" | "str" | "string":
                    forced_value = str(value)
                case "<class 'bytes'>" | "bytes":
                    if isinstance(value, str):
                        forced_value = bytes(value.encode())
                    elif isinstance(value, Integer):
                        forced_value = value.to_bytes()
                    elif isinstance(value, float):
                        forced_value = struct.pack('f', value)
                    elif isinstance(value, bool):
                        forced_value = struct.pack('?', value)
                case _:
                    raise base_exception

        except Exception as e:
            raise base_exception from e

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
        return str(self._value)

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value}, type={self.get_type_str()})"
    
    def __eq__(self, other: 'BaseValue') -> bool:
        if not isinstance(other, BaseValue):
            return False
        return self.hash_leaf() == other.hash_leaf()
    
    @override
    def hash_leaf(self) -> str:
        """Hashes the representation of the base value
        
        Returns:
            str: The hash of the base value
            
        Examples:
            >>> value = BaseValue(1)
            >>> value.hash_leaf()
            '5176a0db25fa8911b84f16b90d6c02d56d0c983122bc26fd137713aa0ede123f'"""
        return MerkleTree.hash_func(repr(self))
