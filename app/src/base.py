import itertools
import hashlib
from abc import ABCMeta, abstractmethod, ABC
from attrs import define, field, validators, converters
from typing import TypeAlias, Optional


number: TypeAlias = int | float
text: TypeAlias = str | bytes
named_container: TypeAlias = dict
linear_container: TypeAlias = list | tuple | set | frozenset
containers: TypeAlias = named_container | linear_container
object_: TypeAlias = object | None
unit_value_types: TypeAlias = number | text
key_value: TypeAlias = tuple[unit_value_types, unit_value_types]
unit_types: TypeAlias = unit_value_types | containers | object_


def hash_sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

class Node:
    def __init__(self, value: unit_types, left: Optional["Node"] = None, right: Optional["Node"] = None):
        self.value = value
        self.left = left
        self.right = right


@define(slots=True, weakref_slot=False)
class BaseInterface(ABC):
    """
    Base interface for all classes
    """
    def _get_slots(self):
        for slot in self.__slots__:
            yield slot

    def __iter__(self):
        yield from self._get_slots()


def _convert_container_to_value(item: unit_types) -> unit_value_types:
    """
    Converts container to value
    """
    item_to_return: unit_value_types = item
    if isinstance(item, linear_container):
        print(Exception("Passed a container, but expected a value, returning the first value of the container"))

        if isinstance(item, list | tuple):
            item_to_return = item[0]

        elif isinstance(item, set):
            item_to_return = item.pop()

        elif isinstance(item, frozenset):
            item_to_return = set(item).pop()

    elif isinstance(item, named_container):
        print(Exception("Passed a container, but expected a value, returning the first value of the container"))
        item_to_return = item[list(item.keys())[0]]

    return item_to_return


@define(frozen=True, slots=True, weakref_slot=False)
class BaseValue[T: unit_types](BaseInterface):
    """
    Base class for all classes
    """
    
    _value: unit_value_types = field(validator=validators.instance_of(unit_types), converter=_convert_container_to_value)

    @property
    def value(self) -> unit_value_types:
        return self._value

    def __str__(self) -> str:
        return str(self._value)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.__str__()})"

def _convert_container_to_base_values(item: unit_types) -> tuple[BaseValue]:
    """
    Converts container to base values
    """
    item_to_return: tuple[BaseValue] = item
    if isinstance(item, linear_container):
        print(Exception("Passed a container of values, but expected a container of base values, a tuple of BaseValue will be returned"))

        if isinstance(item, list | tuple):
            item_to_return = tuple([BaseValue(value) for value in item])

        elif isinstance(item, set):
            item_to_return = tuple([BaseValue(item.pop())])

        elif isinstance(item, frozenset):
            item_to_return = tuple([BaseValue(set(item).pop())])

    elif isinstance(item, named_container):
        item_to_return = tuple([BaseValue(value) for value in item.values()])

    return item_to_return

def _convert_container_to_type(item: unit_types) -> TypeAlias | type:
    return type(item)

@define(slots=True, weakref_slot=False)
class BaseContainer(BaseInterface):
    """
    Base class for all classes
    """
    _items: tuple[BaseValue] = field(validator=validators.deep_iterable(validators.instance_of(unit_types)), converter=_convert_container_to_base_values)
    _type: Optional[type] = field(validator=validators.optional(validators.instance_of(unit_types)), default=None, init=False)

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        self._type = _convert_container_to_type(args[0])
        self._items = _convert_container_to_base_values(args[0])

    @property
    def items(self) -> tuple[BaseValue]:
        return self._items
    
    @property
    def type(self) -> TypeAlias | type:
        return self._type
    

    

