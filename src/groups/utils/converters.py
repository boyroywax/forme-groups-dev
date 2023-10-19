import struct
from typing import Any, Optional, TypeVar, Union

from ..base.types import BaseValueTypes, BaseValueTypesTuple


def convert_to_bytes(value: BaseValueTypes) -> BaseValueTypes:
    """Converts a value to bytes

    Args:
        value (BaseValueTypes): The value to convert
    """
    forced_value: Any = None
    if isinstance(value, str):
        forced_value = bytes(value.encode())
    elif isinstance(value, int):
        forced_value = value.to_bytes()
    elif isinstance(value, float):
        forced_value = struct.pack('f', value)
    elif isinstance(value, bool):
        forced_value = struct.pack('?', value)
    else:
        raise TypeError(f"Could not convert {value} to bytes")
    return forced_value


def force_value_type(value: BaseValueTypes, type_alias: str) -> BaseValueTypes:
    pass
