import struct
from typing import TypeAlias, override, Any, Union, Generic, TypeVar
from attrs import define, field


from .types import BaseTypes, BaseValueTypes, BaseContainerTypes, AllBaseValueTypesTuple, AllBaseValueTypes, AllBaseContainerTypes
from .interface import BaseInterface
from .exceptions import GroupBaseValueException
from ..utils.crypto import MerkleTree


def _base_value_validator(instance, attribute, value):
    """Validates the argument is a BaseValueTypes

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        GroupBaseValueException: If the value is not a BaseValueTypes
    """
    # print(f'{instance=}, {attribute=}, {value=}')
    if not isinstance(value, AllBaseValueTypes):
        raise GroupBaseValueException(f"Expected a value, but received {type(value)}")

# base_type_vars = TypeVar("base_type_vars", int, float, str, bytes, bool, None)


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValue(BaseInterface):
# class BaseValue(BaseInterface, Generic[base_type_vars]):
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
    _value: AllBaseValueTypes = field(validator=_base_value_validator)

    @property
    # def value(self) -> T:
    def value(self) -> AllBaseValueTypes:
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
    def value(self) -> AllBaseValueTypes:
    # def value(self) -> AllBaseValueTypes:
        """The single base value held by the BaseValue Class
        """
        # print(base_type_vars.__constraints__, self._value, type(self._value))
        # print(f'{repr(T)}=')
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
            if value.get_type_str() == type_alias:
                return value

            value = value.value

        assert isinstance(value, AllBaseValueTypes), f"Expected a value, but received {type(value)}"
        forced_value: Any = None

        base_exception: GroupBaseValueException = GroupBaseValueException(f"Could not force value {value} to type {type_alias}")

        try:
            match type_alias:
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
                    elif isinstance(value, int):
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

    def _hash_value(self) -> str:
        return MerkleTree._hash_func(repr(self.value))

    def _hash_type(self) -> str:
        return MerkleTree._hash_func(self.get_type_str())

    def _hash(self) -> MerkleTree:
        # print(self._hash_value(), self._hash_type())
        return MerkleTree(hashed_data=(self._hash_value(), self._hash_type(), ))

    def _verify_hash_value[T: str](self, hash_value: T) -> bool:
        return self._hash_value() == hash_value

    def _verify_hash_type(self, hash_type: str) -> bool:
        return self._hash_type() == hash_type

    def _verify_hash(self, hash_: str) -> bool:
        return self._hash().root() == hash_
