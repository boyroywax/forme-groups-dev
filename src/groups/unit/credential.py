from unittest.mock import Base
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
        default=BaseContainer(('0x000', ), "tuple")
    )

    @property
    def credential(self) -> BaseContainer | None:
        return self._credential
    
    def _to_dict(self):
        return {
            "credential": self.credential._to_dict()
        }
    
    @classmethod
    def _from_dict(cls, data):
        return cls(
            credential=BaseContainer._from_dict(data["credential"])
        )