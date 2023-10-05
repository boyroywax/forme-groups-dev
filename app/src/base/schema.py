from attrs import define, field, validators
from typing import Any

from .interface import BaseInterface
from .container import BaseContainer
from .types import type_set, key_value, type_containers_dict, schema, containers, text



@define(slots=True, weakref_slot=False)
class BaseSchema(BaseInterface):
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

    def _sub_schema(self) -> list[schema]:
        sub_schemas: list['BaseSchema' | str] = []
        for key, value in self._schema.items():
            if isinstance(value, BaseSchema):
                sub_schemas.append({key: value})
            elif isinstance(value, str):
                if value.startswith("schema:"):
                    sub_schemas.append({key: value})

        return sub_schemas

    def _sub_containers(self) -> list[type_containers_dict]:
        sub_units: list[type_containers_dict] = []
        for key, value in self._schema.items():
            if isinstance(value, BaseContainer):
                sub_units.append({key: value})
            if isinstance(value, text):
                if value.startswith("list") or value.startswith("tuple") or value.startswith("set") or value.startswith("frozenset") or value.startswith("dict") or isinstance(value, containers):
                    sub_units.append({key: value})

        return sub_units
    
    def _unpack_schema(self, schema: 'BaseSchema') -> schema:
        schema_unpacked: dict[str, Any] = {}
        for item in iter(schema):
            for key, value in item.items():
                schema[key] = value
        return schema_unpacked
    
    def _get_key_types_from_schema(self) -> set[key_value]:
        key_types: tuple[key_value] = ()
        for dict_ in iter(self):
            for key, value in dict_.items():
                if isinstance(value, type(self).__class__):
                    unpacked = self._unpack_schema(value)
                    key_types = key_types + ((item, ) for item in unpacked)
                else:
                    key_types = key_types + (value, )
            # print(key_types)
        return set(key_types)

    def _unpack_strings(self, type_strings: text) -> text:
        print(f'is_text_instance {type_strings}')
        returned_type_strings: text = ""
        if type_strings.startswith("schema:"):
            returned_type_strings = "schema"
        elif type_strings.startswith("list["):
            returned_type_strings = type_strings[5:-1]
        elif type_strings.startswith("tuple[") or type_strings.startswith("tuple("):
            returned_type_strings = type_strings[6:-1]
        elif type_strings.startswith("set[") or type_strings[:-1].startswith("set{") or type_strings[:-1].startswith("set("):
            returned_type_strings = type_strings[4:-1]
        elif type_strings.startswith("frozenset({") or type_strings.startswith("frozenset(") or type_strings.startswith("frozenset["):
            returned_type_strings = type_strings[11:-1].replace("frozenset({", "").replace("})", "") or type_strings[10:-1].replace("frozenset[", "")
        elif type_strings.startswith("dict{") or type_strings.startswith("dict["):
            returned_type_strings = type_strings[5:-1]
        else:
            returned_type_strings = type_strings
        
        print(f'is_text_instance_returned {returned_type_strings}')
        
        return returned_type_strings

    def _verify_base_types(self, base_types: list[text]) -> (bool, text | None):
        verified: bool = True
        err_msg: text | None = ""

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
    
    def _get_values_from_string_tuple(self, types: text) -> list[text]:
        if self._unpack_strings(types) != types:
            return self._get_values_from_string_tuple(self._unpack_strings(types))
        if ", " in types:
            return types.split(", ")
        if "," in types:
            return types.split(",")
        else:
            return [types]
    
    def _fully_unpack_types(self, types: list[text]) -> list[text]:
        valid_unpacked: list[text] = []
        for key_type in types:
            unpacked = self._unpack_strings(key_type)
            print(f'unpacked {unpacked}')
            if unpacked != key_type:
                split_types = self._get_values_from_string_tuple(unpacked)
                print(f'split_types {split_types}')
                
            #     return self._fully_unpack_types([unpacked])
            # else:
            #     if "," not in unpacked:
            #         valid_unpacked.append(unpacked)
            #     else:
            #         for item in unpacked.split(", "):
            #             valid_unpacked.append(self._fully_unpack_types(item))

            # if unpacked == key_type:
            #     if "," not in unpacked:
            #         valid_unpacked.append(unpacked)
            #     else:

            #     else:
            #         for item in key_type.split(","):
            #             valid_unpacked.append(self._fully_unpack_types(item))
            # else:
            #     valid_unpacked.append(self._fully_unpack_types(unpacked))
        return valid_unpacked



    def _verify_schema(self) -> (bool, str | None):
        """
        Verifies that the schema is valid
        """
        invalid_types: list[text] = []
        valid_types: list[text] = []
        verified: bool = True
        err_msg: str | None = ""

        key_types: type_set = self._get_key_types_from_schema()
        valid_types = self._fully_unpack_types(list(key_types))

        verified, err_msg = self._verify_base_types(valid_types)

        return verified, err_msg

    def __iter__(self):
        for key, value in self._schema.items():
            if isinstance(value, BaseSchema):
                yield {key: "schema"}
                yield from [item for item in iter(value)]
            else:
                yield {key: value}

