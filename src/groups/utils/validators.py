from types import NoneType
from typing import Any
from ..base.types import BaseValueType, LinearContainer, NamedContainer, BaseContainerType
from ..base.exceptions import GroupBaseValueException


def _is_base_value_type(item: Any) -> bool:
    """
    Checks if item is a base value

    Args:
        item (BaseValueTypes): The item to check
    """
    return isinstance(item, BaseValueType)


def validate_base_value_type(instance, attribute, value) -> None:
    """Validates the argument is a BaseValueTypes

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        GroupBaseValueException: If the value is not a BaseValueTypes
    """
    if not _is_base_value_type(value):
        raise GroupBaseValueException(f"Expected a BaseValueTypes, but received {value}, which is of type {type(value)}")


def is_base_container_type(item: Any) -> bool:
    """
    Checks if item is a base container
    """
    return isinstance(item, BaseContainerType)


def is_linear_container(item: Any) -> bool:
    """
    Checks if item is a linear container
    """
    return isinstance(item, LinearContainer)


def is_named_container(item: Any) -> bool:
    """
    Checks if item is a named container
    """
    return isinstance(item, NamedContainer)


def contains_sub_container(item: Any) -> bool:
    """
    Checks if container contains a sub container
    """
    # assert is_base_container_type(item), f"Expected a container, but received a non-container {item}"

    if is_linear_container(item):
        for value in item:
            return is_base_container_type(value)

    elif is_named_container(item):
        for value in item.values():
            return is_base_container_type(value)

    return False