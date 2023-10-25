from attrs import define, field, validators
from typing import Optional

from ..base.interface import BaseInterface
from ..base.container import BaseContainer


@define(frozen=True, slots=True, weakref_slot=False)
class Owner(BaseInterface):
    """The Owner class holds the owner of the Group Unit
    """

    _owner: Optional[BaseContainer] = field(
        validator=validators.optional(validators.instance_of(BaseContainer)),
        default=BaseContainer(('0x000', ), "tuple"))

    @property
    def owner(self) -> BaseContainer | None:
        return self._owner
    
    def _to_dict(self):
        return {
            "owner": self.owner._to_dict() if self.owner is not None else []
        }
    
    @classmethod
    def _from_dict(cls, data):
        return cls(
            owner=BaseContainer._from_dict(data["owner"]) if data["owner"] else BaseContainer(('0x000', ), "tuple")
        )

