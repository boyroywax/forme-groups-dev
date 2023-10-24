from attrs import define, field, validators, Factory
from typing import Optional

from .unit import GroupUnit, Credential, Data, Owner, Nonce
from .pool import Pool


@define(slots=True, weakref_slot=False)
class Controller:
    """The Controller class holds a Pool of Group Units and is used to manage the Group Units

    Args:
        pool (Optional[Pool]): The Pool of Group Units
    """
    pool: Optional[Pool] = field(
        default=Factory(Pool),
        validator=validators.optional(validators.instance_of(Pool)))
    
    _active: Optional[GroupUnit] = field(
        default=Factory(GroupUnit),
        validator=validators.optional(validators.instance_of(GroupUnit)))

    def __init__(self, pool: Optional[Pool] = None):
        if pool is not None:
            self.pool = pool
        else:
            self.pool = Pool()

        self._active = pool.group_units[-1][1]

    @property
    def active(self) -> GroupUnit | None:
        return self._active
    
    @active.setter
    def active(self, value: GroupUnit):
        self._active = value

    def _add_group_unit(self, group_unit: GroupUnit) -> None:
        """Adds a GroupUnit to the Pool

        Args:
            group_unit (GroupUnit): The GroupUnit to add to the Pool
        """
        self.pool.add_group_unit(group_unit)

    def _create_group_unit(self, data: Data) -> GroupUnit:
        """Creates a GroupUnit

        Args:
            data (Data): The Data of the GroupUnit

        Returns:
            GroupUnit: The created GroupUnit
        """
        nonce = self.active.nonce._next_active_nonce()
        credential = Credential()
        owner = Owner()
        group_unit = GroupUnit(nonce, owner, credential, data)
        self._add_group_unit(group_unit)
        return group_unit

    def _get_group_unit(self, hash_: str) -> GroupUnit:
        """Gets a GroupUnit from the Pool

        Args:
            hash_ (str): The hash_ of the GroupUnit to get from the Pool

        Returns:
            GroupUnit: The GroupUnit from the Pool
        """
        return self.pool.get_group_unit(hash_)

