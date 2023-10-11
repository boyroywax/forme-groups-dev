from attrs import define, field, validators
from typing import Optional, TypeAlias, TypeVar


from .interface import BaseInterface
from .types import BaseValueTypes, UnitTypes, NamedContainer, LinearContainer, BaseContainerTypes
from .value import BaseValue
from .exceptions import GroupBaseContainerException


def _base_container_validator(instance, attribute, value):
    """Validates the argument is a BaseContainerTypes

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        GroupBaseContainerException: If the value is not a BaseContainerTypes
    """
    if not isinstance(value, BaseContainerTypes().all):
        raise GroupBaseContainerException(f"Expected a container, but received {type(value)}")
    if len(value) == 0:
        raise GroupBaseContainerException(f"Expected a non-empty container, but received {type(value)}")
    
    


def _base_container_default() -> tuple[BaseValue]:
    """The default factory for BaseContainer

    Returns:
        tuple[BaseValue]: The default factory for BaseContainer
    """
    return tuple()


def _base_container_converter(value: BaseContainerTypes().all) -> tuple[BaseValue]:
    """The converter for BaseContainer

    Args:
        value (tuple[BaseValue]): The value to convert

    Returns:
        tuple[BaseValue]: The converted value
    """
    return tuple(BaseValue(value=value_) for value_ in value)


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainer[T: BaseContainerTypes().all](BaseInterface):

    _items: tuple[BaseValue] = field(
        validator=validators.deep_iterable(validators.instance_of(BaseValue), iterable_validator=validators.instance_of(BaseContainerTypes().all)),
        converter=_base_container_converter
    )
    _type_alias: BaseContainerTypes().all = T


