from attrs import define, field, validators
from typing import Optional, TypeAlias, Type, override

from ..base.interface import BaseInterface
from ..base.container import BaseContainer


@define(frozen=True, slots=True, weakref_slot=False)
class Credential(BaseInterface):
    """The Credential class holds the Group Unit Credential
    """

    _credential: BaseContainer = field(
        validator=validators.instance_of(BaseContainer),
    )

    @property
    def credential(self) -> BaseContainer:
        return self._credential