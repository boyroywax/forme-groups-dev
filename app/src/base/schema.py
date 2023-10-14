from attrs import define, field, validators
from typing import Any

from .interface import BaseInterface
from .container import BaseContainer
from .types import TextSet, KeyValue, TextContainersDict, BaseSchemaType, BaseContainerTypes, Text, LinearContainer, NamedContainer



@define(slots=True, weakref_slot=False)
class BaseSchemaType(BaseInterface):
    """
    Describes the data structure of a container
    Data Schemas can be nested

    Example Schema:
    ```python
    address_schema = {
        "street": "string",
        "city": "string",
        "state": "string",
        "zip": "string"
    }
    person_schema = {
        "name": "string",
        "age": "number",
        "address": "schema:address_schema"
    }
    ```
    """
    _schema: dict[str, Any] = field(validator=validators.instance_of(dict))

    def __init__(self, schema: BaseSchemaType):
        self._schema = schema
        self._verify_schema()


    def _sub_schema(self, schema_: BaseSchemaType = None) -> list[BaseSchemaType]:
        sub_schemas: list['BaseSchemaType' | str] = []
        schema_to_scan: BaseSchemaType = schema_ is not None or self._schema
        for key, value in schema_to_scan.items():
            if isinstance(value, BaseSchemaType):
                sub_schemas.append({key: value})
            elif isinstance(value, str):
                if value.startswith("schema:"):
                    sub_schemas.append({key: value})

        return sub_schemas

    def _sub_containers(self, schema_: BaseSchemaType | Text = None) -> list[TextContainersDict]:
        sub_units: list[TextContainersDict] = []
        print(f'schema_ {schema_}')
        schema_to_scan: BaseSchemaType = schema_._schema if schema_ is not None else self._schema
        print(f'schema_to_scan {schema_to_scan}')
        for key, value in schema_to_scan.items():
            if isinstance(value, BaseContainer):
                sub_units.append({key: value})
            if isinstance(value, Text | BaseContainerTypes):
                print(f'value {value}')
                if value.startswith("list") or value.startswith("tuple") or value.startswith("set") or value.startswith("frozenset") or value.startswith("dict") or isinstance(value, BaseContainerTypes):
                    sub_units.append({key: value})
            if isinstance(value, BaseSchemaType):
                sub_units.extend(self._sub_containers(value))

        return sub_units

    def _unpack_schema(self, schema: 'BaseSchemaType') -> BaseSchemaType:
        schema_unpacked: dict[str, Any] = {}
        for item in iter(schema):
            for key, value in item.items():
                # schema_unpacked[key] = f'{schema.__name__()}.{value}'
                schema_unpacked[key] = value
        return schema_unpacked

    def _get_key_types_from_schema(self) -> set[KeyValue]:
        key_types: tuple[KeyValue] = ()
        for dict_ in iter(self):
            for key, value in dict_.items():
                if isinstance(value, LinearContainer):
                    unpacked = self._unpack_schema(value)
                    key_types = key_types + ((item, ) for item in unpacked)
                elif isinstance(value, NamedContainer):
                    raise Exception(f"Named containers are not supported, use a sub schema instead. Convert {key} to a schema and embed it in the parent schema.")
                else:
                    key_types = key_types + (value, )
        return set(key_types)

    @staticmethod
    def _unpack_strings(type_strings: Text) -> Text:
        # print(f'is_text_instance {type_strings}')
        returned_type_strings: Text = ""
        if type_strings.startswith("schema:"):
            returned_type_strings = "schema"
        elif type_strings.startswith("list["):
            returned_type_strings = type_strings[5:-1]
        elif type_strings.startswith("tuple[") or type_strings.startswith("tuple("):
            returned_type_strings = type_strings[6:-1]
        elif type_strings.startswith("set[") or type_strings[:-1].startswith("set{") or type_strings[:-1].startswith("set("):
            returned_type_strings = type_strings[4:-1]
        elif type_strings.startswith("frozenset({") or type_strings.startswith("frozenset(") or type_strings.startswith("frozenset["):
            returned_type_strings = type_strings[11:-1] or type_strings[10:-1]
        elif type_strings.startswith("dict{") or type_strings.startswith("dict["):
            returned_type_strings = type_strings[5:-1]
        else:
            returned_type_strings = type_strings

        # print(f'is_text_instance_returned {returned_type_strings}')

        if returned_type_strings == type_strings:
            return returned_type_strings
        else:
            return BaseSchemaType._unpack_strings(returned_type_strings)

    @staticmethod
    def _verify_base_types(base_types: list[Text]) -> (bool, Text | None):
        verified: bool = True
        err_msg: Text | None = ""

        for key_type in base_types:
            match (key_type):
                case("schema" | "schema:"):
                    continue
                case("bool" | "boolean"):
                    continue
                case("int" | "integer"):
                    continue
                case("float" | "number"):
                    continue
                case("str" | "string"):
                    continue
                case("bytes" | "byte"):
                    continue
                case(_):
                    verified = False
                    err_msg += f"Key type '{key_type}' is not valid. "

        return verified, err_msg

    @staticmethod
    def _get_values_from_string_tuple(types: Text) -> list[Text]:
        if ", " in types:
            return types.split(", ")
        if "," in types:
            return types.split(",")
        if " ," in types:
            return types.split(" ,")
        if " , " in types:
            return types.split(" , ")
        else:
            return [types]

    @staticmethod
    def _fully_unpack_types(types: list[Text]) -> list[Text]:
        # print(f'types {types}')
        valid_unpacked: list[Text] = []
        for key_type in types:
            unpacked = BaseSchemaType._unpack_strings(key_type)

            if "," in unpacked:
                split_types = BaseSchemaType._get_values_from_string_tuple(unpacked)

                if len(split_types) >= 1:
                    for split_type in split_types:
                        units = BaseSchemaType._fully_unpack_types([split_type])
                        # print(f'units {units}')
                        valid_unpacked = valid_unpacked + units
            else:
                valid_unpacked.append(unpacked)

        return valid_unpacked

    def _verify_schema(self) -> (bool, str | None):
        """
        Verifies that the schema is valid
        """
        valid_types: list[Text] = []
        verified: bool = True
        err_msg: str | None = ""

        key_types: TextSet = self._get_key_types_from_schema()
        valid_types = self._fully_unpack_types(list(key_types))
        # print(f'valid_types {valid_types}')
        verified, err_msg = self._verify_base_types(valid_types)

        return verified, err_msg

    def __iter__(self):
        for key, value in self._schema.items():
            if isinstance(value, BaseSchemaType):
                yield {key: "schema"}
                yield from [item for item in iter(value)]
            else:
                yield {key: value}

    def __str__(self) -> str:
        processed_string: str = ""
        for dict_ in iter(self):
            for key, value in dict_.items():
                processed_string += f"{key}: {value}, "

        return processed_string[:-2]
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" + "(schema={" + str(self) + "})"

    def __name__(self) -> str:
        return self.__class__.__name__
