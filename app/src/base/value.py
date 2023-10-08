from attrs import define, field, validators
from typing import override, Any, Union


from .types import UnitValueTypes, UnitTypes, Number
from .interface import BaseInterface
# from ..utils.converters import _convert_container_to_value
from ..utils.crypto import MerkleTree


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValue[T: UnitValueTypes](BaseInterface):
    """Base class for values
    """
    _value: T = field(validator=validators.instance_of(UnitValueTypes))

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
        """
        if isinstance(value, BaseValue):
            return value.value

        raise TypeError(f"Expected a BaseValue, but received {type(value)}")
    
    @staticmethod
    def _force_type(value: Union["BaseValue", UnitValueTypes], type_: str) -> 'BaseValue':
        """Forces a value to a type

        Args:
            value (unit_value_types): The value to force
            type_ (unit_types): The type to force the value to

        Returns:
            unit_value_types: The forced value
        """
        if isinstance(value, BaseValue):
            if value.get_type_str() == type_:
                return value
            
            value = value.value

        assert isinstance(value, UnitValueTypes), f"Expected a value, but received {type(value)}"
        forced_value: Any = None

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
                    elif isinstance(value, Number):
                        forced_value = value.to_bytes()
                    else:
                        forced_value = bytes(value)
                case _:
                    raise TypeError(f"Could not force value {value} to type {type_}")

        except Exception as e:
            raise TypeError(f"Could not force value {value} to type {type_}") from e

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
        return MerkleTree.hash_func(repr(self))
