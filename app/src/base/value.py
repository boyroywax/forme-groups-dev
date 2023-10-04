from attrs import define, field, validators

from .types import unit_value_types, unit_types
from .interface import BaseInterface
from ..utils.converters import _convert_container_to_value


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValue[T: unit_value_types](BaseInterface):
    """
    Base class for all classes
    """
    
    _value: T = field(validator=validators.instance_of(unit_types), converter=_convert_container_to_value)

    @property
    def value(self) -> T:
        return self._value

    def __str__(self) -> str:
        return str(self._value)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.__str__()})"
