"""
The Schema declares the structure of the data that is being stored in a Container.


"""

from attrs import define, field, validators
from typing import Any, TypeAlias

from .interface import BaseInterface
from .types import BaseValueTypes, BaseContainerTypes
from .container import BaseContainer
from .value import BaseValue


@define(frozen=True, slots=True, weakref_slot=False)
class SchemaEntry(BaseInterface):
    _key: str = field(validator=validators.instance_of(str))
    _value: type | TypeAlias = field(validator=validators.instance_of(str | BaseValueTypes().all | BaseContainerTypes().all))


@define(slots=True, weakref_slot=False)
class BaseSchema(BaseInterface):
    _schema: tuple[SchemaEntry, ...] = field(validator=validators.deep_iterable(validators.instance_of(SchemaEntry), iterable_validator=validators.instance_of(tuple)))
    

