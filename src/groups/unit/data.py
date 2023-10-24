from attrs import define, field, validators
from typing import Optional, Tuple

from ..utils.crypto import MerkleTree

from ..base.value import BaseValue
from ..base.types import BaseContainerTypes, BaseValueTypes
from ..base.interface import BaseInterface
from ..base.container import BaseContainer
from ..base.schema import BaseSchema


def _convert_to_entry(item: BaseContainer | BaseValue | BaseContainerTypes | BaseValueTypes ) -> BaseContainer:
    """Converts the given item to a BaseContainer

    Args:
        item (BaseContainer | tuple[BaseContainer, BaseSchema]): The item to convert

    Returns:
        BaseContainer: The converted item
    """
    if isinstance(item, BaseContainer):
        return item
    elif isinstance(item, BaseValue):
        return BaseContainer((item,))
    elif isinstance(item, BaseContainerTypes):
        return BaseContainer(item)
    elif isinstance(item, BaseValueTypes):
        return BaseContainer((BaseValue(item),))
    else:
        raise TypeError(f"Expected a BaseContainer, but received {type(item)}")
    

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

    entry: BaseContainer = field(
        validator=validators.instance_of(BaseContainer),
        converter=_convert_to_entry)

    schema: Optional[BaseSchema] = field(
        validator=validators.optional(validators.instance_of(BaseSchema)),
        default=None)
    
    @property
    def has_schema(self) -> bool:
        return self.schema is not None
    
    def _num_entries(self) -> int:
        return len(self.entry.items)
    
    @staticmethod
    def _get_schema_of_data_entry(data_entry: BaseContainer) -> Tuple[str, ...]:
        """Returns the types of the data entry

        Returns:
            Tuple[str, ...]: The types of the data entry
        """
        types_: Tuple[str, ...] = tuple()
        for value in data_entry.items:
            types_ += (value.get_type_str(),)
        return types_
    
    @staticmethod
    def _check_if_data_entry_matches_schema(data_entry: BaseContainer, schema_: BaseSchema) -> bool:
        """Checks if the data entry matches the schema entry

        Args:
            data_entry (BaseContainer): The data entry to check
            schema_entry (BaseSchema): The schema entry to check

        Returns:
            bool: True if the data entry matches the schema entry, False otherwise
        """
        exc_msg = f"Expected data entry to match schema entry, but received {data_entry} and {schema_}"

        i: int = 0
        for type_ in Data._get_schema_of_data_entry(data_entry):
            if type_ != schema_.entries[0]._str_value(schema_.entries[i]._value):
                print(f'Expected {type_} to be {schema_.entries[0]._str_value(schema_.entries[i]._value)}')
                raise TypeError(exc_msg)
            i += 1
        return True
    
    @classmethod
    def _from(cls, entry: BaseContainer, schema: Optional[BaseSchema] = None, schema_to_enforce: Optional[BaseSchema] = None) -> 'Data':
        """Creates a Data object from the given data and schema

        Args:
            data (BaseContainer): The data to create the Data object from
            schema (Optional[BaseSchema], optional): The schema to create the Data object from. Defaults to None.

        Returns:
            Data: The Data object created from the given data and schema
        """
        if schema is not None:
            assert isinstance(schema, BaseSchema), f"Expected a BaseSchema, but received {type(schema)}"
            
        if schema_to_enforce is not None:
            assert isinstance(schema_to_enforce, BaseSchema), f"Expected a BaseSchema, but received {type(schema_to_enforce)}"
        
            assert Data._check_if_data_entry_matches_schema(entry, schema_to_enforce), f"Expected data to match schema, but received {entry} and {schema}"

        return cls(entry=entry, schema=schema)
    
    def _hash(self) -> MerkleTree:
        return self.entry._hash()
