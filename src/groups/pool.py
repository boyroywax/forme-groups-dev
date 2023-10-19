from attrs import define, field, validators, Factory
from typing import Tuple, Optional, override

from .unit import GroupUnit


def _validate_group_unit_entry(instance, attr, value: tuple[str, GroupUnit]) -> tuple[str, GroupUnit]:
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
        default=Factory(tuple),
        validator=validators.optional(validators.deep_iterable(_validate_group_unit_entry,
        iterable_validator=validators.instance_of(tuple))))
    
    def _quick_check_if_exists(self, package_hash: str) -> bool:
        """Check if a GroupUnit exists in the Pool

        Args:
            package_hash (str): The package_hash of the GroupUnit to check if it exists in the Pool

        Returns:
            bool: True if the GroupUnit exists in the Pool, False otherwise
        """
        for item in self.group_units:
            if item[0] == package_hash:
                return True
        return False
    
    def check_if_exists(self, group_unit: GroupUnit) -> bool:
        """Check if a GroupUnit exists in the Pool

        Args:
            group_unit (GroupUnit): The GroupUnit to check if it exists in the Pool

        Returns:
            bool: True if the GroupUnit exists in the Pool, False otherwise
        """
        package_hash: str = group_unit._hash_package().root()

        return self._quick_check_if_exists(package_hash)
    
    def add_group_unit(self, group_unit: GroupUnit) -> None:
        """Add a GroupUnit to the Pool

        Args:
            group_unit (GroupUnit): The GroupUnit to add to the Pool

        Raises:
            TypeError: If group_unit is not a GroupUnit
        """
        if not isinstance(group_unit, GroupUnit):
            raise TypeError(f'Expected GroupUnit, got {type(group_unit)}')

        group_unit_hash: str = group_unit._hash_package().root()

        if self._quick_check_if_exists(group_unit_hash):
            raise ValueError(f'GroupUnit with package_hash {group_unit_hash} already exists in the Pool')

        self.group_units += ((group_unit_hash, group_unit), )

    @override
    def __iter__(self):
        return iter(self.group_units)

    @override
    def __repr__(self):
        return f'Pool(group_units={self.group_units})'
