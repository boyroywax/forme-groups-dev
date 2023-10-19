import struct
from typing import Any, Optional, TypeVar, Union

from ..base.types import BaseValueTypes, BaseValueTypesTuple


def convert_to_bytes(value: BaseValueTypes) -> bytes:
    """Converts a value to bytes

    Args:
        value (BaseValueTypes): The value to convert
    """
    if isinstance(value, str):
        return bytes(value.encode())
    elif isinstance(value, int):
        return value.to_bytes()
    elif isinstance(value, float):
        return struct.pack('f', value)
    elif isinstance(value, bool):
        return struct.pack('?', value)
    else:
        raise TypeError(f"Could not convert {value} to bytes")


def convert_to_str(value: Any) -> str:
    """Converts a value to str

    Args:
        value (BaseValueTypes): The value to convert
    """

    if isinstance(value, bytes):
        return str(struct.unpack('b', value)[0])
    elif isinstance(value, (int, float, bool)):
        return str(value)
    else:
        raise TypeError(f"Could not convert {value} to str")


def convert_to_int(value: Any) -> int:
    """Converts a value to int

    Args:
        value (BaseValueTypes): The value to convert
    """
    if isinstance(value, (str, int, float, bool)):
        return int(value)
    elif isinstance(value, bytes):
        return int.from_bytes(value, 'big')
    else:
        raise TypeError(f"Could not convert {value} to int")


def convert_to_float(value: Any) -> float:
    """Converts a value to float

    Args:
        value (BaseValueTypes): The value to convert
    """
    if isinstance(value, (str, int, float, bool)):
        return float(value)
    elif isinstance(value, bytes) and len(value) == 4:
        return struct.unpack('f', value)[0]
    else:
        raise TypeError(f"Could not convert {value} to float")
    

def convert_to_bool(value: Any) -> bool:
    """Converts a value to bool

    Args:
        value (BaseValueTypes): The value to convert
    """
    if isinstance(value, (str, int, float, bool)):
        return bool(value)
    elif isinstance(value, bytes):
        return struct.unpack('?', value)[0]
    else:
        raise TypeError(f"Could not convert {value} to bool")


def force_value_type(value: BaseValueTypes, type_alias: str) -> BaseValueTypes:
    assert isinstance(value, BaseValueTypes), f"Expected a value, but received {type(value)}"
    assert isinstance(type_alias, str), f"Expected a string, but received {type(type_alias)}"

    if value is None:
        return None

    match type_alias:
        case "<class 'NoneType'>" | "NoneType" | "None":
            return None
        case "<class 'bool'>" | "bool" | "boolean":
            return convert_to_bool(value)
        case "<class 'int'>" | "int" | "integer":
            return convert_to_int(value)
        case "<class 'float'>" | "float":
            return convert_to_float(value)
        case "<class 'str'>" | "str" | "string":
            return convert_to_str(value)
        case "<class 'bytes'>" | "bytes":
            return convert_to_bytes(value)
        case _:
            raise TypeError(f"Could not force value {value} to type {type_alias}")

