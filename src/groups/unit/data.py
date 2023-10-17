from attrs import define, field, validators
from typing import Optional, TypeAlias, Type, override

from ..base.types import LinearContainer, NamedContainer, AllBaseContainerTypes
from ..base.interface import BaseInterface
from ..base.value import BaseValue
from ..base.container import BaseContainer
from ..base.schema import BaseSchema
from ..base.exceptions import GroupBaseException
from ..utils.crypto import MerkleTree


@define(frozen=True, slots=True, weakref_slot=False)
class Data(BaseInterface):
    _schema: Optional[BaseSchema] = field(
        validator=validators.optional(validators.instance_of(BaseSchema)),
    )

    _entry: BaseContainer = field(
        validator=validators.instance_of(BaseContainer),
    )

    @property
    def data(self) -> BaseContainer:
        return self._entry
