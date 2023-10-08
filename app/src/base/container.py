from attrs import define, field, validators
from typing import Optional, TypeAlias

from .interface import BaseInterface
from .types import UnitValueTypes, UnitTypes, NamedContainer, LinearContainer, Containers
from .value import BaseValue
from .exceptions import GroupBaseContainerException
from ..utils.converters import _convert_container_to_default, _convert_container_to_type

@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainer(BaseInterface):
    """
    Base class for all classes
    """
    _items: tuple[BaseValue] = field(validator=validators.deep_iterable(validators.instance_of(UnitTypes)))
    _type: Optional[type] = field(validator=validators.optional(validators.instance_of(UnitTypes)), default=None)

    def __attrs_init__(self, *args, **kwargs):
        print(args, kwargs)
        items_ = kwargs.get("items", None) or kwargs.get("_items", None) or args[0] if len(args) > 0 else None
        self._items = self._extract_base_values(items_)

        type_ = kwargs.get("type", None) or kwargs.get("_type", None) or args[1] if len(args) > 1 else None
        if type_ is None:
            self._type = _convert_container_to_type(args[0])
        else:
            self._type = type_

    @property
    def items(self) -> tuple[BaseValue]:
        return self._items

    @property
    def type(self) -> TypeAlias | type:
        return self._type

    @staticmethod
    def _contains_sub_container(item: Containers | UnitValueTypes) -> bool:
        """
        Checks if container contains a sub container
        """
        if isinstance(item, BaseValue | UnitValueTypes):
            return False

        elif isinstance(item, LinearContainer | BaseContainer | NamedContainer):
            return True

        else:
            raise GroupBaseContainerException(f"Passed a value, but expected a container. {item}")
        
    @staticmethod
    def _extract_base_values(item: Containers) -> tuple[BaseValue]:
        """
        Converts container to base values
        """
        items_to_return: tuple[BaseValue] = tuple()
        if isinstance(item, LinearContainer):
            print(Exception("Passed a container of values, but expected a container of base values, a tuple of BaseValue will be returned"))

            if isinstance(item, list | tuple):
                items_to_return = tuple([BaseValue(value) for value in item])

            elif isinstance(item, set):
                items_to_return = tuple([BaseValue(item.pop()) for _ in range(len(item))])

            elif isinstance(item, frozenset):
                items = set(item)
                items_to_return = tuple([BaseValue(items.pop()) for _ in range(len(items))])

        elif isinstance(item, NamedContainer):
            items_to_return: tuple[BaseValue] = tuple()
            for key, value in item.items():
                items_to_return += (BaseValue(key), BaseValue(value))
            print(items_to_return)

        return items_to_return

    @staticmethod
    def _unpack_container(item: Containers, depth: int = 1) -> tuple[BaseValue]:
        """
        Unpacks the container to depth
        """
        unpacked_items: tuple[BaseValue] = tuple()

        if depth >= 1:
            if isinstance(item, BaseValue | UnitValueTypes):
                return (item, )

            elif BaseContainer._contains_sub_container(item):
                unpacked_items = unpacked_items + BaseContainer._extract_base_values(item)
                for value in BaseContainer._iter_all_(item):
                    unpacked_items = unpacked_items + BaseContainer._unpack_container(value, depth - 1)

        return unpacked_items

    @staticmethod
    def _iter_all_(item: Containers | UnitValueTypes):
        """
        Checks if container contains a sub container
        """
        if isinstance(item, BaseValue | UnitValueTypes):
            yield item

        elif isinstance(item, LinearContainer | BaseContainer):
            for value in item:
                yield BaseContainer._unpack_container(value)

        elif isinstance(item, NamedContainer):
            for key, value in item.items():
                yield BaseContainer._unpack_container(value)
                yield BaseContainer._unpack_container(key)

    def _package(self) -> UnitTypes:
        return _convert_container_to_default(self._items, self._type)

    def __iter__(self):
        yield from self._items

    def __str__(self) -> str:
        return str(self._package())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={[item for item in iter(self)]}, type={self._type})"
