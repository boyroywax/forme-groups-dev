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
