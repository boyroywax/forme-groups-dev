from abc import ABC, abstractmethod
from attrs import define, field, validators
from enum import Enum
from typing import Any, Union, TypeAlias, TypeVar, Type, Tuple, Optional, Callable, override

from .interface import BaseInterface
from .exceptions import GroupBaseTypeException


# @define(frozen=True, slots=True, weakref_slot=False)
# class BaseTypeVars:
#     Integer: TypeVar = TypeVar('Integer', bound=int)
#     FloatingPoint = TypeVar('FloatingPoint', bound=float)
#     Boolean = TypeVar('Boolean', bound=bool)
#     String = TypeVar('String', bound=str)
#     Bytes = TypeVar('Bytes', bound=bytes)
#     Number = TypeVar('Number', bound=Union[int, float])
#     Text = TypeVar('Text', bound=Union[str, bytes, bool, None])
#     Dictionary = TypeVar('Dictionary', bound=dict)
#     List = TypeVar('List', bound=list)
#     Tuple = TypeVar('Tuple', bound=tuple)
#     Set = TypeVar('Set', bound=set)
#     FrozenSet = TypeVar('FrozenSet', bound=frozenset)
#     Container = TypeVar('Containers', bound=Union[dict, list, tuple, set, frozenset])
#     Value = TypeVar('Value', bound=Union[int, float, str, bool, None])
#     Typing = TypeVar('Typing', TypeAlias, type)


@define(frozen=True, slots=True, weakref_slot=False)
class BaseTypeInterface(BaseInterface, ABC):
    aliases: Tuple[str, ...] = field(
        validator=validators.deep_iterable(validators.instance_of(str), iterable_validator=validators.instance_of(tuple)),
    )

    super_type: Optional[Tuple[str, ...]] = field(
        validator=validators.optional(validators.instance_of(str | Union[type])),
        default=None
    )

    prefix: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
        default=None
    )

    suffix: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
        default=None
    )

    seperator: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
        default=None
    )

    type_class: Optional[Callable] = field(
        validator=validators.optional(validators.instance_of(type | Union[type | TypeAlias])),
        default=str
    )

    type_var: Optional[TypeVar] = field(
        validator=validators.optional(validators.instance_of(TypeVar)),
        default=None
    )

    constraints: Optional[Union[type, TypeAlias]] = field(
        validator=validators.optional(validators.instance_of(type | TypeAlias)),
        default=None
    )

    @property
    def is_container(self) -> bool:
        """Whether the base type is a container

        Returns:
            bool: Whether the base type is a container
        """
        if self.prefix is not None:
            return True

    def _contains_alias(self, alias: str) -> bool:
        """Checks if type contains an alias

        Args:
            type_ (str): The type to check

        Returns:
            bool: Whether the type contains an alias
        """
        for alias_ in self.aliases:
            if alias == alias_:
                return True
            if alias_.contains(alias):
                raise GroupBaseTypeException(f"Alias {alias} is a substring of {alias_}, and should be removed")
        
    def _check_for_errors(self):
        """Checks for errors in the base type"""
        if self.prefix is not None and self.suffix is not None:
            if self.prefix == self.suffix:
                raise GroupBaseTypeException(f"Prefix and suffix cannot be the same: {self.prefix}")
            
        if self.prefix is None and self.suffix is not None:
            raise GroupBaseTypeException(f"Prefix cannot be None if suffix is not None: {self.prefix}")
        
        if self.prefix is not None and self.suffix is None and self.seperator is not None:
            raise GroupBaseTypeException(f"Seperator cannot be used if prefix is not None and suffix is None: {self.seperator}")
        
    def _type_to_string(self, type_: TypeAlias | type) -> str:
        """Converts a type to a string

        Args:
            type_ (TypeAlias | type): The type to convert

        Returns:
            str: The type as a string
        """
        if isinstance(type_, type):
            return type_.__name__
        else:
            return type_
        
    @override
    def __str__(self) -> str:
        return self._aliases[0]
    

@define(frozen=True, slots=True, weakref_slot=False)
class BaseTypePool(BaseInterface):
    Integer = BaseTypeInterface(
        aliases=(
            str("Integer"), "integer", "INTEGER",
            str("Int"), str("int"), "INT",
            "IntegerType", "integer_type", "INTEGER_TYPE",
            "IntType", "int_type", "INT_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_INT__",
        type_class=int,
        type_var=TypeVar('Integer', bound=int),
        constraints=int
    )

    FloatingPoint = BaseTypeInterface(
        aliases=(
            str("FloatingPoint"), "floating_point", "FLOATING_POINT",
            str("Float"), str("float"), "FLOAT",
            "FloatingPointType", "floating_point_type", "FLOATING_POINT_TYPE",
            "FloatType", "float_type", "FLOAT_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_FLOAT__",
        type_class=float,
        type_var=TypeVar('FloatingPoint', bound=float),
        constraints=float
    )

    Boolean = BaseTypeInterface(
        aliases=(
            str("Boolean"), "boolean", "BOOLEAN",
            str("Bool"), str("bool"), "BOOL",
            "BooleanType", "boolean_type", "BOOLEAN_TYPE",
            "BoolType", "bool_type", "BOOL_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_BOOL__",
        type_class=bool,
        type_var=TypeVar('Boolean', bound=bool),
        constraints=bool
    )

    String = BaseTypeInterface(
        aliases=(
            str("String"), "string", "STRING",
            str("Str"), str("str"), "STR",
            "StringType", "string_type", "STRING_TYPE",
            "StrType", "str_type", "STR_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_STR__",
        type_class=str,
        type_var=TypeVar('String', bound=str),
        constraints=str
    )

    Bytes_ = BaseTypeInterface(
        aliases=(
            str("Bytes"), "bytes", "BYTES",
            "BytesType", "bytes_type", "BYTES_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_BYTES__",
        type_class=bytes,
        type_var=TypeVar('Bytes', bound=bytes),
        constraints=bytes
    )

    # Number = BaseTypeInterface(
    #     aliases=(
    #         str("Number"), "number", "NUMBER",
    #         "NumberType", "number_type", "NUMBER_TYPE"
    #     ),
    #     super_type=None,
    #     type_class=Union[int, float],
    #     type_var=TypeVar('Number', bound=Union[int, float]),
    #     constraints=Union[int, float]
    # )

    # Text = BaseTypeInterface(
    #     aliases=(
    #         str("Text"), "text", "TEXT",
    #         "TextType", "text_type", "TEXT_TYPE"
    #     ),
    #     super_type=Union[str, bytes, bool, None],
    #     type_class=Union[str, bytes, bool, None],
    #     type_var=TypeVar('Text', bound=Union[str, bytes, bool, None]),
    #     constraints=Union[str, bytes, bool, None]
    # )
        
    


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
            # for alias in types:
            #     if item == alias:
            return item in types.values()
                    # return True

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
    """Holds the base value types for the Group Base Value Types"""
    integer: TypeAlias = int
    floating_point: TypeAlias = float
    boolean: TypeAlias = bool
    string: TypeAlias = str
    bytes_: TypeAlias = bytes
    number: TypeAlias = int | float
    text: TypeAlias = str | bytes | bool | None
    # _all: TypeAlias = field(default=int | float | str | bytes | bool | None)

    @property
    def all(self) -> BaseTypeVars.Container:
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
        aliases: dict[type | TypeAlias, tuple[str, ...]] = {
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
    def _is_container_type(value: Any) -> bool:
        """Verifies that a value is a base container type

        Args:
            value (Any): The value to verify

        Returns:
            bool: Whether the value is a base container type
        """
        return isinstance(value, BaseContainerTypes().all)


AllBaseValueTypes = BaseValueTypes().all
AllBaseContainerTypes = BaseContainerTypes().all
LinearContainer = BaseContainerTypes().linear
NamedContainer = BaseContainerTypes().named
BaseValueContainer = tuple[AllBaseValueTypes]

# Base Object Types
Object = object | None
KeyValue = tuple[BaseValueTypes().all, BaseValueTypes().all]
UnitTypes = BaseValueTypes().all | BaseContainerTypes().all | Object
Text = BaseValueTypes().text
TextSet = set[BaseValueTypes().text]
TextOrContainer = BaseValueTypes().text | BaseContainerTypes().all
TextContainersDict = dict[BaseValueTypes().text, BaseContainerTypes().all]

# Base Schema Types
BaseSchemaType = dict[BaseValueTypes().text, Any]