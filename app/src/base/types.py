from enum import Enum
from typing import TypeAlias, Any, Union


# Base Value Types
Integer: TypeAlias = int
FloatingPoint: TypeAlias = float
Boolean: TypeAlias = bool
String: TypeAlias = str
Bytes: TypeAlias = bytes
Number: TypeAlias = Union[Integer, FloatingPoint]
Text: TypeAlias = Union[String, Bytes, Boolean,  None]
BaseValueTypes: TypeAlias = Union[Number, Text]

# Base Container Types
NamedContainer: TypeAlias = dict
LinearContainer: TypeAlias = list | tuple | set | frozenset
BaseContainerTypes: TypeAlias = NamedContainer | LinearContainer
Object: TypeAlias = object | None
KeyValue: TypeAlias = tuple[BaseValueTypes, BaseValueTypes]
UnitTypes: TypeAlias = BaseValueTypes | BaseContainerTypes | Object
TextSet: TypeAlias = set[Text]
TextOrContainer: TypeAlias = Text | BaseContainerTypes
TextContainersDict: TypeAlias = dict[Text, Text | BaseContainerTypes]

# Base Schema Types
BaseSchema: TypeAlias = dict[Text, Any]