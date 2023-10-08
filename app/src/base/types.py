from typing import TypeAlias, Any


Integer: TypeAlias = int
Boolean: TypeAlias = bool
String: TypeAlias = str

Number: TypeAlias = Integer | float
Text: TypeAlias = String | bytes | Boolean | None
NamedContainer: TypeAlias = dict
LinearContainer: TypeAlias = list | tuple | set | frozenset
Containers: TypeAlias = NamedContainer | LinearContainer
Object: TypeAlias = object | None
UnitValueTypes: TypeAlias = Number | Text
KeyValue: TypeAlias = tuple[UnitValueTypes, UnitValueTypes]
UnitTypes: TypeAlias = UnitValueTypes | Containers | Object
TextSet: TypeAlias = set[Text]
TextOrContainer: TypeAlias = Text | Containers
TextContainersDict: TypeAlias = dict[Text, Text | Containers]
BaseSchema: TypeAlias = dict[Text, Any]
