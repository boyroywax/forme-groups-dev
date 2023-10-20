from attrs import define, field, validators
from typing import Optional

from ..base.interface import BaseInterface
from ..base.container import BaseContainer
from ..base.schema import BaseSchema


@define(frozen=True, slots=True, weakref_slot=False)
class Data(BaseInterface):
    """The Data class holds the Group Unit's Data

        Notes:
            The Schema defines the data structure of the Group Unit on the sub level of the Group Unit
            The Data is a BaseContainer object, which holds the data of the Group Unit.
            Data in this Group Unit is verified by the schema of the Group Unit a level above.
    
        Args:
            entry (BaseContainer): The entry of the Data
            schema (Optional[BaseSchema]): The schema of the Data

        Raises:
            TypeError: If entry is not a BaseContainer
            TypeError: If schema is not a BaseSchema
    """

    _entry: BaseContainer = field(
        validator=validators.instance_of(BaseContainer))

    _schema: Optional[BaseSchema] = field(
        validator=validators.optional(validators.instance_of(BaseSchema)),
        default=None)

    @property
    def data(self) -> BaseContainer:
        return self._entry
    
    @property
    def schema(self) -> Optional[BaseSchema]:
        return self._schema
    
    @property
    def has_schema(self) -> bool:
        return self._schema is not None
    
    def _num_entries(self) -> int:
        return len(self._entry.items)
