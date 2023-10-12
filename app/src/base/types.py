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
    def all(self) -> Union[type, TypeAlias]:
        """The base types

        Returns:
            type | TypeAlias: The base types
        """

    @property
    @abstractmethod
    def aliases(self) -> dict[type | TypeAlias, tuple[str]]:
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

        return False

    def _get_type_from_alias(self, alias: str) -> type:
        """Gets the type from an alias

        Args:
            alias (str): The alias to get the type from

        Returns:
            BaseValueTypes.all: The type from the alias
        """
        for type_, aliases in self.aliases.items():
            # print(type_, aliases)
            for alias_ in aliases:
                if alias == alias_:
                    # print(type_)
                    return type_


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValueTypes(BaseTypesInterface):
    """BHolds the base value types for the Group Base Value Types"""
    integer: TypeAlias = int
    floating_point: TypeAlias = float
    boolean: TypeAlias = bool
    string: TypeAlias = str
    bytes_: TypeAlias = bytes
    number: TypeAlias = int | float
    text: TypeAlias = str | bytes | bool | None
    # _all: TypeAlias = field(default=int | float | str | bytes | bool | None)

    @property
    def all(self) -> Union[type, TypeAlias]:
        return Union[self.number, self.text]

    @property
    def aliases(self) -> dict[type | TypeAlias, tuple[str]]:
        """The aliases for the base value types

        Returns:
            dict[str, tuple[str]]: The aliases for the base value types
        """
        aliases: dict = {
            self.integer: (
                str("Integer"), "integer", "INTEGER",
                str("Int"), str("int"), "INT",
                "IntegerType", "integer_type", "INTEGER_TYPE",
                "IntType", "int_type", "INT_TYPE"
            ),
            self.floating_point: (
                str("FloatingPoint"), "floating_point", "FLOATING_POINT",
                str("Float"), str("float"), "FLOAT",
                "FloatingPointType", "floating_point_type", "FLOATING_POINT_TYPE",
                "FloatType", "float_type", "FLOAT_TYPE"
            ),
            self.boolean: (
                str("Boolean"), "boolean", "BOOLEAN",
                str("Bool"), str("bool"), "BOOL",
                "BooleanType", "boolean_type", "BOOLEAN_TYPE",
                "BoolType", "bool_type", "BOOL_TYPE"
            ),
            self.string: (
                str("String"), "string", "STRING",
                str("Str"), str("str"), "STR",
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
        if isinstance(value, BaseValueTypes().all):
            return True
        return False


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainerTypes(BaseTypesInterface):
    """Holds the base container types for the Group Base Container Types"""
    dictionary: TypeAlias = dict
    list_: TypeAlias = list
    tuple_: TypeAlias = tuple
    set_: TypeAlias = set
    frozenset_: TypeAlias = frozenset
    named: TypeAlias = dictionary
    linear: TypeAlias = list_ | tuple_ | set_ | frozenset_

    @property
    def all(self) -> Union[type,  TypeAlias]:
        """The base container types"""
        return Union[self.named, self.linear]

    @property
    def aliases(self) -> dict[type | TypeAlias, tuple[str]]:
        aliases: dict[type | TypeAlias, tuple[str]] = {
            self.dictionary: (
                str("Dictionary"), "dictionary", "DICTIONARY",
                str("Dict"), str("dict"), "DICT",
                # "DictionaryType", "dictionary_type", "DICTIONARY_TYPE",
                "DictType", "dict_type", "DICT_TYPE"
            ),
            self.list_: (
                str("List"), "list", "LIST",
                "ListType", "list_type", "LIST_TYPE"
            ),
            self.tuple_: (
                str("Tuple"), "tuple", "TUPLE",
                "TupleType", "tuple_type", "TUPLE_TYPE"
            ),
            self.set_: (
                str("Set"), "set", "SET",
                "SetType", "set_type", "SET_TYPE"
            ),
            self.frozenset_: (
                str("FrozenSet"), "frozenset", "FROZENSET",
                "FrozenSetType", "frozenset_type", "FROZENSET_TYPE"
            ),
            # self.named: (
            #     str("Named"), "named", "NAMED",
            #     str("NamedContainer"), "named_container", "NAMED_CONTAINER",
            #     "NamedContainerType", "named_container_type", "NAMED_CONTAINER_TYPE"
            # ),
            self.linear: (
                str("Linear"), "linear", "LINEAR",
                str("LinearContainer"), "linear_container", "LINEAR_CONTAINER",
                "LinearContainerType", "linear_container_type", "LINEAR_CONTAINER_TYPE"
            ),
            self.all: (
                str("BaseContainer"), "base_container", "BASE_CONTAINER",
                str("BaseContainerTypes"), "base_container_types", "BASE_CONTAINER_TYPES",
                str("BaseContainerType"), "base_container_type", "BASE_CONTAINER_TYPE"
            )
        }
        return aliases

    @staticmethod
    def _verify_base_container_type(value: Any) -> bool:
        """Verifies that a value is a base container type

        Args:
            value (Any): The value to verify

        Returns:
            bool: Whether the value is a base container type
        """
        if isinstance(value, BaseContainerTypes().all):
            return True

        return False


# # Base Object Types
# Object = object | None
# KeyValue = tuple[BaseValueTypes.all, BaseValueTypes.all]
# UnitTypes = BaseValueTypes.all | BaseContainerTypes.all | Object
# TextSet = set[BaseValueTypes.Text]
# TextOrContainer = BaseValueTypes.Text | BaseContainerTypes.all
# TextContainersDict = dict[BaseValueTypes.Text, BaseContainerTypes.all]

# # Base Schema Types
# BaseSchema = dict[BaseValueTypes.Text, Any]