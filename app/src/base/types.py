from abc import ABC, abstractmethod
from attrs import define, field, validators
from typing import Any, Union, TypeAlias

from .interface import BaseInterface
from .exceptions import GroupBaseTypeException
from ..utils.crypto import MerkleTree


@define(frozen=True, slots=True, weakref_slot=False)
class BaseTypesInterface(BaseInterface, ABC):
    """Base interface for all Base Type classes"""
    
    @property
    @abstractmethod
    def all(self) -> Union[TypeAlias, TypeAlias]:
        """The base types

        Returns:
            type | TypeAlias: The base types
        """

    @property
    @abstractmethod
    def aliases(self) -> dict[str, tuple[str]]:
        """The aliases for the base types

        Returns:
            dict[str, tuple[str]]: The aliases for the base types
        """

    @staticmethod
    def _type_contains_alias(type_: tuple[str], alias: str) -> bool:
        """Checks if type contains an alias

        Args:
            type_ (str): The type to check

        Returns:
            bool: Whether the type contains an alias
        """
        for alias_ in type_:
            if alias == alias_:
                return True
            if alias_.contains(alias):
                raise GroupBaseTypeException(f"Alias {alias} is a substring of {alias_}, and should be removed")

    def _contains_alias(self, item: Any) -> bool:
        """Checks if item is a base value type

        Args:
            item (Any): The item to check

        Returns:
            bool: Whether the item is a base value type
        """
        for types in self.aliases.values():
            for alias in types:
                if item == alias:
                    return True
            break
        else:
            return False

    def _get_type_from_alias(self, alias: all) -> type:
        """Gets the type from an alias

        Args:
            alias (str): The alias to get the type from

        Returns:
            BaseValueTypes.all: The type from the alias
        """
        for types in self.aliases:
            for alias_ in types:
                if alias == alias_:
                    return types
            break
        else:
            raise GroupBaseTypeException(f"Could not find type for alias {alias}")


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValueTypes(BaseTypesInterface):
    """BHolds the base value types for the Group Base Value Types"""
    integer: TypeAlias = field(default=int)
    floating_point: TypeAlias = field(default=float)
    boolean: TypeAlias = field(default=bool)
    string: TypeAlias = field(default=str)
    bytes_: TypeAlias = field(default=bytes)
    number: TypeAlias = field(default=int | float)
    text: TypeAlias = field(default=str | bytes | bool | None)
    _all: TypeAlias = field(default=int | float | str | bytes | bool | None)

    @property
    def all(self) -> Union[TypeAlias, TypeAlias]:
        return self._all

    @property
    def aliases(self) -> dict[type | TypeAlias, tuple[str]]:
        """The aliases for the base value types

        Returns:
            dict[str, tuple[str]]: The aliases for the base value types
        """
        aliases: dict = {
            self.integer: (
                str("Integer"), "integer", "INTEGER",
                str("Int"), str("Int"), "INT",
                "IntegerType", "integer_type", "INTEGER_TYPE",
                "IntType", "int_type", "INT_TYPE"
            ),
            self.floating_point: (
                str("FloatingPoint"), "floating_point", "FLOATING_POINT",
                str("Float"), str("Float"), "FLOAT",
                "FloatingPointType", "floating_point_type", "FLOATING_POINT_TYPE",
                "FloatType", "float_type", "FLOAT_TYPE"
            ),
            self.boolean: (
                str("Boolean"), "boolean", "BOOLEAN",
                str("Bool"), str("Bool"), "BOOL",
                "BooleanType", "boolean_type", "BOOLEAN_TYPE",
                "BoolType", "bool_type", "BOOL_TYPE"
            ),
            self.string: (
                str("String"), "string", "STRING",
                str("Str"), str("Str"), "STR",
                "StringType", "string_type", "STRING_TYPE",
                "StrType", "str_type", "STR_TYPE"
            ),
            self.bytes_: (
                str("Bytes"), "bytes", "BYTES",
                "BytesType", "bytes_type", "BYTES_TYPE"
            ),
            self.number: (
                str("Number"), "number", "NUMBER",
                "NumberType", "number_type", "NUMBER_TYPE"
            ),
            self.text: (
                str("Text"), "text", "TEXT",
                "TextType", "text_type", "TEXT_TYPE"
            ),
            self.all: (
                str("BaseValueTypes"), "base_value_types", "BASE_VALUE_TYPES",
                str("BaseValueType"), "base_value_type", "BASE_VALUE_TYPE"
            )
        }
        return aliases

    @staticmethod
    def _verify_base_value_type(value: Any) -> bool:
        """Verifies that a value is a base type

        Args:
            value (Any): The value to verify

        Returns:
            bool: Whether the value is a base type
        """
        if isinstance(value, BaseValueTypes.all):
            return True
        else:
            return False


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainerTypes(BaseTypesInterface):
    """Holds the base container types for the Group Base Container Types"""
    dictionary: TypeAlias = field(default=dict)
    list_: TypeAlias = field(default=list)
    tuple_: TypeAlias = field(default=tuple)
    set_: TypeAlias = field(default=set)
    frozenset_: TypeAlias = field(default=frozenset)
    named_container: TypeAlias = dict
    linear_container: TypeAlias = list | tuple | set | frozenset

    @property
    def all(self) -> type | TypeAlias:
        """The base container types"""
        return self.named_container | self.linear_container

    @property
    def aliases(self) -> dict[type | TypeAlias, tuple[str]]:
        aliases: dict = {
            "named_container": (
                str("NamedContainer"), "named_container", "NAMED_CONTAINER",
                "NamedContainerType", "named_container_type", "NAMED_CONTAINER_TYPE"
            ),
            "linear_container": (
                str("LinearContainer"), "linear_container", "LINEAR_CONTAINER",
                "LinearContainerType", "linear_container_type", "LINEAR_CONTAINER_TYPE"
            ),
            "base_container_type": (
                str("BaseContainerTypes"), "base_container_types", "BASE_CONTAINER_TYPES",
                str("BaseContainerType"), "base_container_type", "BASE_CONTAINER_TYPE"
            )
        }
        return aliases


# # Base Object Types
# Object = object | None
# KeyValue = tuple[BaseValueTypes.all, BaseValueTypes.all]
# UnitTypes = BaseValueTypes.all | BaseContainerTypes.all | Object
# TextSet = set[BaseValueTypes.Text]
# TextOrContainer = BaseValueTypes.Text | BaseContainerTypes.all
# TextContainersDict = dict[BaseValueTypes.Text, BaseContainerTypes.all]

# # Base Schema Types
# BaseSchema = dict[BaseValueTypes.Text, Any]