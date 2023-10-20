from attrs import define, field, validators

from ..base.interface import BaseInterface
from .credential import Credential
from .data import Data
from .owner import Owner
from .nonce import Nonce


@define(frozen=True, slots=True, weakref_slot=False)
class GroupUnit(BaseInterface):
    """The Group Unit class holds the Group Unit data
    """

    nonce: Nonce = field(
        validator=validators.instance_of(Nonce))

    owner: Owner = field(
        validator=validators.instance_of(Owner))

    credential: Credential = field(
        validator=validators.instance_of(Credential))

    data: Data = field(
        validator=validators.instance_of(Data))


__all__ = ["GroupUnit", "Credential", "Data", "Owner", "Nonce"]
