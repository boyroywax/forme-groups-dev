from attrs import define, field, validators
from typing import Optional
from ..base.interface import BaseInterface
from ..base.container import BaseContainer


@define(frozen=True, slots=True, weakref_slot=False)
class Credential(BaseInterface):
    """The Credential class holds the Group Unit Credential
    """

    _credential: Optional[BaseContainer] = field(
        validator=validators.optional(validators.instance_of(BaseContainer)),
        default=None
    )

    @property
    def credential(self) -> BaseContainer | None:
        return self._credential