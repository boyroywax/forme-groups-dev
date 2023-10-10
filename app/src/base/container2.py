from attrs import define, field, validators
from typing import Optional, TypeAlias, TypeVar


from .interface import BaseInterface
from .types import BaseValueType, UnitTypes, NamedContainer, LinearContainer, BaseContainerTypes
from .value import BaseValue
from .exceptions import GroupBaseContainerException


def _


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainer(BaseInterface):
    
    _items: tuple[BaseValue] = field(validator=validators.deep_iterable(validators.instance_of(UnitTypes)))
    _type: TypeVar = 