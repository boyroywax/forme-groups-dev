from attrs import define, field, validators
from typing import Tuple, Optional

from .unit import GroupUnit


def _validate_group_unit_entry(value: tuple[str, GroupUnit]) -> tuple[str, GroupUnit]:
    if not isinstance(value, tuple):
        raise TypeError(f'Expected tuple, got {type(value)}')

    if len(value) != 2:
        raise ValueError(f'Expected tuple of length 2, got {len(value)}')

    if not isinstance(value[0], str):
        raise TypeError(f'Expected str, got {type(value[0])}')

    if not isinstance(value[1], GroupUnit):
        raise TypeError(f'Expected GroupUnit, got {type(value[1])}')

    return value


@define(slots=True, weakref_slot=False)
class Pool:
    """The Pool class holds the Group Pool data
    """
    group_units: Optional[Tuple[Tuple[str, GroupUnit], ...]] = field(
        default=None,
        validator=validators.optional(validators.deep_iterable(validators.deep_iterable(_validate_group_unit_entry,
        iterable_validator=validators.instance_of(tuple)),
        iterable_validator=validators.instance_of(tuple))))
