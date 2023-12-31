from abc import ABC
from enum import Enum
from attrs import define, field, validators
from types import NoneType
from typing import Any, Union, TypeAlias, TypeVar, Type, Tuple, Optional, Callable, override, List, Set, FrozenSet, Dict

from .interface import BaseInterface
from .exceptions import GroupBaseTypeException
from ..utils.crypto import MerkleTree


@define(frozen=True, slots=True, weakref_slot=False)
class BaseType(BaseInterface):
# class BaseType:
    """Base class for types
    
    Args:
        aliases (Tuple[str, ...]): The aliases for the base type
        super_type (Optional[Tuple[str, ...]]): The super type of the base type
        prefix (Optional[str]): The prefix for the base type
        suffix (Optional[str]): The suffix for the base type
        separator (Optional[str]): The separator for the base type
        type_class (Optional[Callable]): The type class for the base type
        type_var (Optional[TypeVar]): The type var for the base type
        constraints (Optional[Union[type, TypeAlias]]): The constraints for the base type
        _encryption_key (Optional[bytes]): The encryption key for the base type
    """
    aliases: Tuple[str, ...] = field(
        validator=validators.deep_iterable(validators.instance_of(str),
        iterable_validator=validators.instance_of(Tuple)))

    super_type: Optional[Tuple[str, ...]] = field(
        validator=validators.optional(validators.instance_of((str, type))),
        default=None)

    prefix: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
        default=None)

    suffix: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
        default=None)

    separator: Optional[str] = field(
        validator=validators.optional(validators.instance_of(str)),
        default=None)

    type_class: Optional[Callable] = field(
        validator=validators.optional(validators.instance_of((type, TypeAlias))),
        default=str)

    type_var: Optional[TypeVar] = field(
        validator=validators.optional(validators.instance_of(TypeVar)),
        default=None)

    constraints: Optional[type | TypeAlias] = field(
        validator=validators.optional(validators.instance_of((type, TypeAlias))),
        default=None)

    _encryption_key: Optional[bytes] = field(
        validator=validators.optional(validators.instance_of(bytes)),
        default=None)

    @property
    def is_container(self) -> bool:
        """Whether the base type is a container

        Returns:
            bool: Whether the base type is a container
        """
        if self.prefix is not None:
            return True
        
        return False
    
    @property
    def separators(self) -> Tuple[str, ...]:
        """The separators for the base type

        Returns:
            Tuple[str]: The separators for the base type
        """
        if self.separator is not None:
            return (self.separator,)
        return tuple(f" {self.separator}", f"{self.separator} ", f" {self.separator} ", f"{self.separator}")
        
    def _contains(self, property: str, query: str, exclude: Optional[Tuple[str, ...]] = None) -> bool:
        assert property in self.__slots__

        match(property):
            case("aliases"):
                if query in self.aliases:
                    return True
                for alias in self.aliases:
                    if exclude is not None:
                        if self.aliases[0] in exclude:
                            continue
                    else:
                        if alias.__contains__(query):
                            raise GroupBaseTypeException(f"Alias {query} is a substring of {alias}, and should be removed")
            case("super_type"):
                if query in self.super_type:
                    return True
            case("separator"):
                if query in self.separators:
                    return True
            case _:
                if query == getattr(self, property):
                    return True
        return False

    def _contains_alias(self, alias: str, exclude: Optional[Tuple[str, ...]] = None) -> bool:
        """Checks if type contains an alias

        Args:
            type_ (str): The type to check

        Returns:
            bool: Whether the type contains an alias
        """
        return self._contains("aliases", alias, exclude)
            
    def _check_for_errors(self) -> None:
        """Checks for errors in the base type"""
        if self.prefix is not None and self.suffix is not None:
            if self.prefix == self.suffix:
                raise GroupBaseTypeException(f"Prefix and suffix cannot be the same: {self.prefix}")
            
        if self.prefix is None and self.suffix is not None:
            raise GroupBaseTypeException(f"Prefix cannot be None if suffix is not None: {self.prefix}")
        
        if self.prefix is not None and self.suffix is None and self.separator is not None:
            raise GroupBaseTypeException(f"Seperator cannot be used if prefix is not None and suffix is None: {self.separator}")
        
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
        """Convert the first Alias to a string
        
        Returns:
            str: The first alias
        """
        return self._aliases[0]
    
    @override
    def __repr__(self) -> str:
        """Convert the first Alias to a string

        """
        return super().__repr_private__(include_underscored_slots=False)
    

@define(frozen=True, slots=True, weakref_slot=False)
class _BaseTypes(BaseInterface):
# class _BaseTypes:
    Integer: BaseType = field(default=BaseType(
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
    ))

    FloatingPoint: BaseType = field(default=BaseType(
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
    ))

    Boolean: BaseType = field(default=BaseType(
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
    ))

    String: BaseType = field(default=BaseType(
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
    ))

    Bytes: BaseType = field(default=BaseType(
        aliases=(
            str("Bytes"), "bytes", "BYTES",
            "BytesType", "bytes_type", "BYTES_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_BYTES__",
        type_class=bytes,
        type_var=TypeVar('Bytes', bound=bytes),
        constraints=bytes
    ))

    Dictionary: BaseType = field(default=BaseType(
        aliases=(
            str("Dictionary"), "dictionary", "DICTIONARY",
            str("Dict"), str("dict"), "DICT",
            # "DictionaryType", "dictionary_type", "DICTIONARY_TYPE",
            "DictType", "dict_type", "DICT_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_DICT__",
        prefix="{",
        suffix="}",
        separator=",",
        type_class=dict,
        type_var=TypeVar('Dictionary', bound=dict),
        constraints=dict
    ))

    List: BaseType = field(default=BaseType(
        aliases=(
            str("List"), "list", "LIST",
            "ListType", "list_type", "LIST_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_LIST__",
        prefix="[",
        suffix="]",
        separator=",",
        type_class=list,
        type_var=TypeVar('List', bound=list),
        constraints=list
    ))

    Tuple: BaseType = field(default=BaseType(
        aliases=(
            str("Tuple"), "tuple", "TUPLE",
            "TupleType", "tuple_type", "TUPLE_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_TUPLE__",
        prefix="(",
        suffix=")",
        separator=",",
        type_class=tuple,
        type_var=TypeVar('Tuple', bound=tuple),
        constraints=tuple
    ))

    Set: BaseType = field(default=BaseType(
        aliases=(
            str("Set"), "set", "SET",
            "SetType", "set_type", "SET_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_SET__",
        prefix="{",
        suffix="}",
        separator=",",
        type_class=set,
        type_var=TypeVar('Set', bound=set),
        constraints=set
    ))

    FrozenSet: BaseType = field(default=BaseType(
        aliases=(
            str("FrozenSet"), "frozenset", "FROZENSET",
            "FrozenSetType", "frozenset_type", "FROZENSET_TYPE"
        ),
        super_type="__SYSTEM_RESERVED_FROZENSET__",
        prefix="{",
        suffix="}",
        separator=",",
        type_class=frozenset,
        type_var=TypeVar('FrozenSet', bound=frozenset),
        constraints=frozenset
    ))

    def all(self, type_: Optional[str] = None, format_: Optional[str] = None) -> Union[type | TypeAlias, tuple[type | TypeAlias, ...]]:
        """All the system types

        Returns:
            type | TypeAlias: All the system types
        """
        assert type_ in ["value", "container", "linear", "named", "text", "number"] or type_ is None
        assert format_ in ["tuple", "union"] or format_ is None

        if type_ is None:
            type_ = "all"

        if format_ is None:
            format_ = "union"

        match (type_, format_):
            case ("value", "union"):
                return Union[
                    self.Integer.type_class,
                    self.FloatingPoint.type_class,
                    self.Boolean.type_class,
                    self.String.type_class,
                    self.Bytes.type_class,
                    None
                ]
            case ("value", "tuple"):
                return (
                    self.Integer.type_class,
                    self.FloatingPoint.type_class,
                    self.Boolean.type_class,
                    self.String.type_class,
                    self.Bytes.type_class,
                    None,
                )
            case ("text", "union"):
                return Union[
                    self.String.type_class,
                    self.Bytes.type_class,
                    self.Boolean.type_class,
                    None
                ]
            case ("text", "tuple"):
                return (
                    self.String.type_class,
                    self.Bytes.type_class,
                    self.Boolean.type_class,
                    None,
                )
            case ("number", "union"):
                return Union[
                    self.Integer.type_class,
                    self.FloatingPoint.type_class
                ]
            case ("number", "tuple"):
                return (
                    self.Integer.type_class,
                    self.FloatingPoint.type_class,
                )
            case ("container", "union"):
                return Union[
                    self.Dictionary.type_class,
                    self.List.type_class,
                    self.Tuple.type_class,
                    self.Set.type_class,
                    self.FrozenSet.type_class
                ]
            case ("container", "tuple"):
                return (
                    self.Dictionary.type_class,
                    self.List.type_class,
                    self.Tuple.type_class,
                    self.Set.type_class,
                    self.FrozenSet.type_class,
                )
            case ("linear", "union"):
                return Union[
                    self.List.type_class,
                    self.Tuple.type_class,
                    self.Set.type_class,
                    self.FrozenSet.type_class
                ]
            case ("linear", "tuple"):
                return (
                    self.List.type_class,
                    self.Tuple.type_class,
                    self.Set.type_class,
                    self.FrozenSet.type_class,
                )
            case ("named", "union"):
                return self.Dictionary.type_class
            case ("named", "tuple"):
                return (self.Dictionary.type_class, )
            case ("all", "union"):
                return Union[
                    self.Integer.type_class,
                    self.FloatingPoint.type_class,
                    self.Boolean.type_class,
                    self.String.type_class,
                    self.Bytes.type_class,
                    self.Dictionary.type_class,
                    self.List.type_class,
                    self.Tuple.type_class,
                    self.Set.type_class,
                    self.FrozenSet.type_class,
                    None
                ]
            case ("all", "tuple"):
                return (
                    self.Integer.type_class,
                    self.FloatingPoint.type_class,
                    self.Boolean.type_class,
                    self.String.type_class,
                    self.Bytes.type_class,
                    self.Dictionary.type_class,
                    self.List.type_class,
                    self.Tuple.type_class,
                    self.Set.type_class,
                    self.FrozenSet.type_class,
                    None,
                )

    @property
    def all_base_types(self) -> tuple[BaseType, ...]:
        system_types: Tuple[BaseType, ...] = ()
        for slot in self.__slots__:
            base_type: BaseType = getattr(self, slot)
            system_types += (base_type,)
        return system_types

    @property
    def value_types(self) -> type | TypeAlias:
        return self.all("value")
    
    @property
    def container_types(self) -> type | TypeAlias:
        return self.all("container")
    
    @property
    def aliases(self) -> tuple[str, ...]:
        """All the aliases for the base types
        
        Returns:
            tuple[str, ...]: All the aliases for the base types
        """
        aliases: Tuple[str, ...] = ()
        for base_type in self.all_base_types:
            aliases += base_type.aliases
        return aliases

    def _already_exists(self, property: str, query_value: str) -> bool:
        """Checks if a property of a base type already exists

        Args:
            property (str): The property to check
            query_value (str): The value to check

        Returns:
            bool: Whether the property of a base type already exists

        Examples:
            >>> BaseTypes._already_exists("aliases", "int")
            True
        """
        for base_type in self.all_base_types:
            if base_type._contains(property, query_value):
                return True
        return False
    
    def _validate_types(self) -> bool:
        """Validates the types of the base types
        """
        for base_type in self.all_base_types:

            # Check for errors in the base type
            base_type._check_for_errors()

            # Check if certain properties of the base type already exist
            # Base Types cannot share the same aliases ("int" and "set" are excluded from throwing an error, as they clash with FloatingPoint and FrozenSet)
            # Base Types cannot share the same type_class
            for base_type_ in self.all_base_types:
                if base_type is not base_type_:
                    # Check that the type_class is not already used
                    if base_type._type_to_string(base_type.type_class) == base_type_._type_to_string(base_type_.type_class):
                        raise GroupBaseTypeException(f"Type {base_type.type_class} is already used by {base_type_}")
                    
                    # Check that the aliases are not already used
                    for alias in base_type.aliases:
                        # system reserved types "int" and "set" are excluded from throwing an error
                        if base_type_._contains_alias(alias, exclude=("int", "INT", str("Set"), str("set"), "SET")):
                            raise GroupBaseTypeException(f"Alias {alias} is already used by {base_type_}")
        return True

    def _get_type(self, property: str, query_value: str) -> BaseType:
        """Gets a base type from a property
        """
        for base_type in self.all_base_types:
            if base_type._contains(property, query_value):
                return base_type
        raise GroupBaseTypeException(f"BaseType with {property} {query_value} does not exist")
    
    def _get_type_from_alias(self, alias: str) -> Type:
        """Gets a base type from an alias
        """
        return self._get_type("aliases", alias).type_class
    
    def _hash_types(self) -> MerkleTree:
        """Hashes the types
        """
        hashed_types: Tuple[str, ...] = ()
        for base_type in self.all_base_types:
            hashed_types += (base_type._hash_package().root(),)
        return MerkleTree(hashed_data=hashed_types)


class BaseTypeAliases(Enum):
    """The TypeAliases Enum holds the aliases of the type
    """
    INTEGER = ("INTEGER", "INT", "Integer", "Int", "integer", "int", "IntegerType", "IntType", "integer_type", "int_type", "INT_TYPE")
    FLOAT = ("FLOAT", "FLOATING_POINT", "Float", "float", "FloatingPoint", "floating_point", "FloatType", "float_type", "FloatingPointType", "floating_point_type", "FLOAT_TYPE", "FLOATING_POINT_TYPE")
    BOOLEAN = ("BOOLEAN", "BOOL", "Boolean", "Bool", "boolean", "bool", "BooleanType", "BoolType", "boolean_type", "bool_type", "BOOL_TYPE")
    STRING = ("STRING", "STR", "String", "Str", "string", "str", "StringType", "StrType", "string_type", "str_type", "STR_TYPE")
    BYTES = ("BYTES", "Bytes", "bytes", "BytesType", "bytes_type", "BYTES_TYPE")
    DICTIONARY = ("DICTIONARY", "DICT", "Dictionary", "Dict", "dictionary", "dict", "DictionaryType", "DictType", "dictionary_type", "dict_type", "DICT_TYPE")
    LIST = ("LIST", "List", "list", "ListType", "list_type", "LIST_TYPE")
    TUPLE = ("TUPLE", "Tuple", "tuple", "TupleType", "tuple_type", "TUPLE_TYPE")
    SET = ("SET", "Set", "set", "SetType", "set_type", "SET_TYPE")
    FROZENSET = ("FROZENSET", "FrozenSet", "frozenset", "FrozenSetType", "frozenset_type", "FROZENSET_TYPE")

    def __contains__(self, alias: str) -> bool:
        """Checks if the alias is in the TypeAliases Enum

        Args:
            alias (str): The alias to check

        Returns:
            bool: Whether the alias is in the TypeAliases Enum
        """
        return alias in self.value

    def __iter__(self):
        """Iterates over the TypeAliases Enum
        """
        for type_aliases in self.__class__:
            yield type_aliases

    def _get_type_from_alias(self, alias: str) -> Type:
        """Gets a base type from an alias
        """
        for type_aliases in self:
            if alias in type_aliases.value:
                return type_aliases.name


# Base Type Categories
BaseTypes = _BaseTypes()

class BaseValueTypes(Enum):
    """The BaseValueTypes Enum holds the types of the BaseValue
    """
    INTEGER = int
    FLOAT = float
    STRING = str
    BOOLEAN = bool
    BYTES = bytes
    TEXT = Union[str, bytes]
    NUMBER = Union[int, float]
    ALL = Union[int, float, str, bool, bytes, NoneType]

BaseValueType: TypeAlias = BaseValueTypes.ALL.value

class BaseContainerTypes(Enum):
    """The BaseContainerTypes Enum holds the types of the BaseContainer
    """
    DICTIONARY = dict
    LIST = list
    TUPLE = tuple
    SET = set
    FROZENSET = frozenset
    LINEAR = Union[list, tuple, set, frozenset]
    NAMED = dict
    ALL = Union[dict, list, tuple, set, frozenset]

BaseContainerType: TypeAlias = BaseContainerTypes.ALL.value

LinearContainer: TypeAlias = BaseContainerTypes.LINEAR.value
NamedContainer: TypeAlias = BaseContainerTypes.NAMED.value
Text: TypeAlias = BaseValueTypes.TEXT.value
Number: TypeAlias = BaseValueTypes.NUMBER.value

# Base Type Aliases in Tuple Format
BaseValueTypesTuple: Tuple[type | TypeAlias, ...] = BaseTypes.all("value", "tuple")
BaseContainerTypesTuple: Tuple[type | TypeAlias, ...] = BaseTypes.all("container", "tuple")

# Base Object Types
Object = object | None
KeyValue = Tuple[BaseValueType, BaseValueType]
UnitTypes = BaseValueType | BaseContainerType | Object

# Base Text Types
TextSet = set[Text]
TextOrContainer = Text | BaseContainerType
TextContainersDict = dict[Text, BaseContainerType]

# Base Schema Types
BaseSchemaType = dict[Text, Any]
