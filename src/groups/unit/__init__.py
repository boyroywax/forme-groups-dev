from attrs import define, field, validators
from typing import Optional, TypeAlias, Type, override

from ..base.interface import BaseInterface
from .data import Data
from .nonce import Nonce


@define(frozen=True, slots=True, weakref_slot=False)
class GroupUnit(BaseInterface):
    """The Group Unit class holds the Group Unit data
    """

    _nonce: Nonce = field(
        validator=validators.instance_of(Nonce),
    )

    _data: Data = field(
        validator=validators.instance_of(Data),
    )

