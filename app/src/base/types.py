from typing import TypeAlias, Any

number: TypeAlias = int | float
text: TypeAlias = str | bytes | bool | None
named_container: TypeAlias = dict
linear_container: TypeAlias = list | tuple | set | frozenset
containers: TypeAlias = named_container | linear_container
object_: TypeAlias = object | None
unit_value_types: TypeAlias = number | text
key_value: TypeAlias = tuple[unit_value_types, unit_value_types]
unit_types: TypeAlias = unit_value_types | containers | object_
type_set: TypeAlias = set[text]
type_container: TypeAlias = text | containers
type_containers_dict: TypeAlias = dict[text, text | containers]
base_schema: TypeAlias = dict[text, Any]