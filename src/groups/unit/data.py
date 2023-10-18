from attrs import define, field, validators
from typing import Optional

from ..base.interface import BaseInterface
from ..base.container import BaseContainer
from ..base.schema import BaseSchema



@define(frozen=True, slots=True, weakref_slot=False)
class Data(BaseInterface):

    _entry: BaseContainer = field(
        validator=validators.instance_of(BaseContainer),
    )

    _schema: Optional[BaseSchema] = field(
        validator=validators.optional(validators.instance_of(BaseSchema)),
        default=None
    )

    @property
    def data(self) -> BaseContainer:
        return self._entry
