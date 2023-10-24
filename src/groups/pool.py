from attrs import define, field, validators, Factory
from typing import Tuple, Optional, override

from .unit import GroupUnit


def _validate_group_unit_entry(instance, attr, value: tuple[str, str, GroupUnit]) -> tuple[str, str, GroupUnit]:
    if not isinstance(value, tuple):
        raise TypeError(f'Expected tuple, got {type(value)}')

    if len(value) != 3:
        raise ValueError(f'Expected tuple of length 2, got {len(value)}')

    if not isinstance(value[0], str):
        raise TypeError(f'Expected str, got {type(value[0])}')
    
    if not isinstance(value[1], str):
        raise TypeError(f'Expected str, got {type(value[1])}')

    if not isinstance(value[2], GroupUnit):
        raise TypeError(f'Expected GroupUnit, got {type(value[1])}')

    return value


@define(slots=True, weakref_slot=False)
class Pool:
    """The Pool class holds the Group Units

    Args:
        group_units (tuple[tuple[str, str, GroupUnit]]): The Group Units held by the Pool
            structure: ((package_hash, nonce_hash, GroupUnit), ...)

    Examples:
        >>> pool = Pool(group_units=(('package_hash', 'nonce_hash', GroupUnit()),))
    """
    group_units: Optional[Tuple[Tuple[str, str, GroupUnit], ...]] = field(
        default=Factory(tuple),
        validator=validators.optional(validators.deep_iterable(_validate_group_unit_entry,
        iterable_validator=validators.instance_of(tuple))))
    
    def _check_if_hash_exists(self, hash_: tuple[str, ...], lookup: str = "all") -> bool:
        """Check if a GroupUnit exists in the Pool

        Args:
            hash_ (tuple[str, ...]): The hash_ of the GroupUnit to check if it exists in the Pool
            lookup (str, optional): The lookup method to use. Defaults to "all".

        Returns:
            bool: True if the GroupUnit exists in the Pool, False otherwise
        """

        assert isinstance(hash_, tuple), f'Expected hash_ to be tuple, got {type(hash_)}'
        assert len(hash_) > 0, f'Expected hash_ to be non-empty tuple, got {len(hash_)}'

        assert lookup in ('unit', 'nonce', 'all'), f'Expected lookup to be package_hash or nonce_hash, got {lookup}'

        for hash_item in hash_:
            for item in self.group_units:
                if item[0] == hash_item and (lookup == 'unit' or lookup == 'all'):
                    return True
                if item[1] == hash_item and (lookup == 'nonce' or lookup == 'all'):
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

        return self._check_if_hash_exists((package_hash, ))
    
    def add_group_unit(self, group_unit: GroupUnit) -> None:
        """Add a GroupUnit to the Pool

        Args:
            group_unit (GroupUnit): The GroupUnit to add to the Pool

        Raises:
            TypeError: If group_unit is not a GroupUnit
        """
        if not isinstance(group_unit, GroupUnit):
            raise TypeError(f'Expected GroupUnit, got {type(group_unit)}')

        group_unit_hash: str | None = group_unit._hash_package().root()
        nonce_hash: str | None = group_unit.nonce._hash().root()

        assert group_unit_hash is not None, f'Expected group_unit_hash to be str, got {type(group_unit_hash)}'
        assert nonce_hash is not None, f'Expected nonce_hash to be str, got {type(nonce_hash)}'

        if self._check_if_hash_exists((group_unit_hash, nonce_hash), lookup='all'):
            raise ValueError(f'GroupUnit with package_hash {group_unit_hash} already exists in the Pool')

        self.group_units += ((group_unit_hash, nonce_hash, group_unit), )

    def get_group_unit(self, hash_: str, lookup: str = "all") -> GroupUnit:
        """Get a GroupUnit from the Pool

        Args:
            hash_ (str): The hash_ of the GroupUnit to get from the Pool
            lookup (str, optional): The lookup method to use. Defaults to "all".

        Returns:
            GroupUnit: The GroupUnit from the Pool

        Raises:
            ValueError: If the GroupUnit does not exist in the Pool
        """
        assert isinstance(hash_, str), f'Expected hash_ to be str, got {type(hash_)}'

        assert lookup in ('unit', 'nonce', 'all'), f'Expected lookup to be package_hash or nonce_hash, got {lookup}'

        for item in self.group_units:
            if item[0] == hash_ and (lookup == 'unit' or lookup == 'all'):
                return item[2]
            if item[1] == hash_ and (lookup == 'nonce' or lookup == 'all'):
                return item[2]
        raise ValueError(f'GroupUnit with hash_ {hash_} does not exist in the Pool')

    def __iter__(self):
        """Iterate over the Group Units in the Pool
        
        Returns:
            iter: An iterator over the Group Units in the Pool
        """
        return iter(self.group_units)

    def __repr__(self):
        """Return the representation of the Pool

        Returns:
            str: The representation of the Pool
        """
        return f'Pool(group_units={self.group_units})'
