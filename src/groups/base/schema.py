"""
The Schema declares the structure of the Group Unit Data.


"""

from attrs import define, field, validators
from typing import Any, TypeAlias

from .interface import BaseInterface
from .types import BaseValueTypes, BaseContainerTypes, AllBaseValueTypes, AllBaseContainerTypes
from .container import BaseContainer
from .value import BaseValue
from ..utils.converters import _base_type_converter


@define(frozen=True, slots=True, weakref_slot=False)
class SchemaEntry(BaseInterface):
    _key: str = field(validator=validators.instance_of(str))
    _value: str | type | TypeAlias = field(validator=validators.instance_of(str | type | TypeAlias), converter=_base_type_converter)


@define(frozen=True, slots=True, weakref_slot=False)
class BaseSchema(BaseInterface):
    _entries: tuple[SchemaEntry, ...] = field(
        validator=validators.deep_iterable(validators.instance_of(SchemaEntry), iterable_validator=validators.instance_of(tuple)),
    )


