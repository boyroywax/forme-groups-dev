import itertools
from attrs import define, field, validators
from typing import Optional, TypeAlias

from .interface import BaseInterface
from .types import unit_value_types, unit_types, named_container, linear_container
from .value import BaseValue
from ..utils.converters import _convert_container_to_default, _convert_container_to_type

@define(slots=True, weakref_slot=False)
class BaseContainer(BaseInterface):
    """
    Base class for all classes
    """
    _items: tuple[BaseValue] = field(validator=validators.deep_iterable(validators.instance_of(unit_types)))
    _type: Optional[type] = field(validator=validators.optional(validators.instance_of(unit_types)), default=None, init=False)

    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        self._type = _convert_container_to_type(args[0])
        self._items = self._extract_base_values(args[0])

    @property
    def items(self) -> tuple[BaseValue]:
        return self._items

    @property
    def type(self) -> TypeAlias | type:
        return self._type

    @staticmethod
    def _extract_base_values(item: unit_types) -> tuple[BaseValue]:
        """
        Converts container to base values
        """
        items_to_return: tuple[BaseValue]
        if isinstance(item, linear_container):
            print(Exception("Passed a container of values, but expected a container of base values, a tuple of BaseValue will be returned"))

            if isinstance(item, list | tuple):
                items_to_return = tuple([BaseValue(value) for value in item])

            elif isinstance(item, set):
                items_to_return = tuple([BaseValue(item.pop()) for _ in range(len(item))])

            elif isinstance(item, frozenset):
                items = set(item)
                items_to_return = tuple([BaseValue(items.pop()) for _ in range(len(items))])

        elif isinstance(item, named_container):
            # keys: tuple[unit_value_types] = tuple(item.keys())
            # values: tuple[unit_value_types] = tuple(item.values())
            items_to_return: tuple[BaseValue] = tuple()
            for key, value in item.items():
                items_to_return += (BaseValue(key), BaseValue(value))
            print(items_to_return)

        return items_to_return


    def _package(self) -> unit_types:
        return _convert_container_to_default(self._items, self._type)

    def __iter__(self):
        yield from self._items

    def __str__(self) -> str:
        return str(self._package())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={[item for item in iter(self)]}, type={self._type})"
