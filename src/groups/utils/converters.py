import struct
from typing import Any, TypeAlias

from ..base.types import BaseTypes, BaseValueType, BaseContainerTypesTuple, BaseValueTypes


__ALLOW_NONE_VALUE__ = True
__DEFAULT_VALUE__ = None


def convert_none_to_default_value(value: Any) -> Any:
    """Converts None to default value

    Args:
        value (Any): The value to convert
    """
    if (value is None or
        value == "None" or
        value == "Null" or
        value == "null" or
        value == "NONE" or
        value == "NULL" or
        value == "" or
        value == " " or
        value == {} or
        value == [] or
        value == () or
        value == set() or
        value == frozenset()
    ):
        if __ALLOW_NONE_VALUE__:
            return __DEFAULT_VALUE__
        
        raise ValueError(
            f"Expected a value, but received {value} which is type {type(value)}"
            f" and __ALLOW_NONE_VALUE__ is set to {__ALLOW_NONE_VALUE__}")
    else:
        return value

def convert_to_bytes(value: Any) -> bytes:
    """Converts a value to bytes

    Args:
        value (BaseValueType): The value to convert
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
        value (BaseValueType): The value to convert
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
        value (BaseValueType): The value to convert
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
        value (BaseValueType): The value to convert
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
        value (BaseValueType): The value to convert
    """
    if isinstance(value, (str, int, float, bool)):
        return bool(value)
    elif isinstance(value, bytes):
        return struct.unpack('?', value)[0]
    else:
        raise TypeError(f"Could not convert {value} to bool")


def force_value_type(value: BaseValueType, type_alias: str) -> BaseValueType:
    assert isinstance(value, BaseValueType), f"Expected a value, but received {type(value)}"
    assert isinstance(type_alias, str), f"Expected a string, but received {type(type_alias)}"

    if value is None or type_alias == "None":
        return None

    type_from_alias: TypeAlias | type = BaseTypes._get_type_from_alias(type_alias)
    # assert isinstance(type_from_alias, BaseValueType), f"Expected a value type, but received {type_alias}"
    assert type_from_alias in BaseValueTypes, f"Expected a value type, but received {type_alias}"

    if isinstance(value, type_from_alias):
        return value

    match (str(type_from_alias)):
        case "<class 'NoneType'>":
            return None
        case "<class 'bool'>":
            return convert_to_bool(value)
        case "<class 'int'>":
            return convert_to_int(value)
        case "<class 'float'>":
            return convert_to_float(value)
        case "<class 'str'>":
            return convert_to_str(value)
        case "<class 'bytes'>":
            return convert_to_bytes(value)
        case _:
            raise TypeError(f"Could not force value {value} to type {type_alias}")


def convert_tuple(container: tuple[Any, ...], type_alias: str):
    """
    Args:
        container tuple(BaseValueType): The container to convert
    """
    exc_msg: str = f"Expected a container, but received {type(container)}"
    assert isinstance(container, tuple), exc_msg
    assert isinstance(type_alias, str), f"Expected a string, but received {type(type_alias)}"

    type_from_alias: TypeAlias | type = BaseTypes._get_type_from_alias(type_alias)
    assert type_from_alias in BaseContainerTypesTuple, exc_msg

    match (str(type_from_alias)):
        case("<class 'list'>"):
            return [value for value in container]
        case("<class 'tuple'>"):
            return tuple([value for value in container])
        case("<class 'set'>"):
            return {value for value in container}
        case("<class 'frozenset'>"):
            return frozenset({value for value in container})
        case("<class 'dict'>"):
            keys: tuple[Any, ...] = container[::2]
            values: tuple[Any, ...] = container[1::2]
            return {key: value for key, value in zip(keys, values)}
        case _:
            raise TypeError(f"Expected a container, but received {type_alias}")


