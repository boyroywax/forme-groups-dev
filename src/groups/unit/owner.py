from attrs import define, field, validators

from ..base.interface import BaseInterface
from ..base.container import BaseContainer


@define(frozen=True, slots=True, weakref_slot=False)
class Owner(BaseInterface):
    """The Owner class holds the owner of the Group Unit
    """

    _owner: BaseContainer = field(
        validator=validators.instance_of(BaseContainer),
    )

    @property
    def owner(self) -> BaseContainer:
        return self._owner

