from attrs import define, field, validators
from typing import Optional, TypeAlias, Type, override

from ..base.types import LinearContainer, NamedContainer, AllBaseContainerTypes


def is_linear_container(item: AllBaseContainerTypes) -> bool:
    """
    Checks if item is a linear container
    """
    return isinstance(item, LinearContainer)


def is_named_container(item: AllBaseContainerTypes) -> bool:
    """
    Checks if item is a named container
    """
    return isinstance(item, NamedContainer)


def is_any_container(item: AllBaseContainerTypes) -> bool:
    """
    Checks if item is any container
    """
    return is_linear_container(item) or is_named_container(item)


def _contains_sub_container(item: AllBaseContainerTypes) -> bool:
    """
    Checks if container contains a sub container
    """
    assert is_any_container(item), f"Expected a container, but received a non-container {type(item)}"

    if is_linear_container(item):
        for value in item:
            return is_any_container(value)

    elif is_named_container(item):
        for value in item.values():
            return is_any_container(value)

    return False