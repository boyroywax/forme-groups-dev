from attrs import define, field, Factory, validators
from typing import Optional

from .unit import GroupUnit, Credential, Data, Owner, Nonce
from .pool import Pool


@define(slots=True, weakref_slot=False)
class Controller:
    """The Manage class holds the Group Manage data
    """
    pool: Pool = field(
        default=Factory(Pool),
        validator=validators.optional(validators.instance_of(Pool)))
    
    _active: Optional[GroupUnit] = field(
        default=None,
        validator=validators.optional(validators.instance_of(GroupUnit)))

    def __init__(self, pool: Optional[Pool] = None):
        if pool is not None:
            self.pool = pool

        self._active = pool.group_units[-1]