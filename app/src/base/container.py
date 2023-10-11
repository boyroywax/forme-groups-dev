from attrs import define, field, validators
from typing import Optional, TypeAlias

from .interface import BaseInterface
from .types import BaseValueTypes, BaseContainerTypes
from .value import BaseValue
from .exceptions import GroupBaseContainerException
from ..utils.converters import _convert_container_to_default, _convert_container_to_type, _extract_base_values

@define(slots=True, weakref_slot=False)
class BaseContainer(BaseInterface):
    """
    Base class for all classes
    """
    _items: tuple[BaseValue] = field(validator=validators.deep_iterable(validators.instance_of(BaseValue | BaseValueTypes().all), iterable_validator=validators.instance_of(BaseContainerTypes().all)), converter=_extract_base_values)
    _type: type | str = field(validator=validators.instance_of(type | str), default=tuple)

    @property
    def items(self) -> tuple[BaseValue]:
        return self._items

    @property
    def type(self) -> TypeAlias | type:
        return self._type

    @staticmethod
    def _contains_sub_container(item: BaseContainerTypes().all | BaseValueTypes().all) -> bool:
        """
        Checks if container contains a sub container
        """
        if isinstance(item, BaseValue | BaseValueTypes().all):
            return False

        elif isinstance(item, BaseContainerTypes().all):
            return True

        else:
            raise GroupBaseContainerException(f"Passed a value, but expected a container. {item}")
        
    @staticmethod
    def _extract_base_values(item: BaseContainerTypes().all) -> tuple[BaseValue]:
        """
        Converts container to base values
        """
        items_to_return: tuple[BaseValue] = tuple()
        if isinstance(item, BaseContainerTypes().linear):
            print(Exception("Passed a container of values, but expected a container of base values, a tuple of BaseValue will be returned"))

            if isinstance(item, list | tuple):
                items_to_return = tuple([BaseValue(value) for value in item])

            elif isinstance(item, set):
                items_to_return = tuple([BaseValue(item.pop()) for _ in range(len(item))])

            elif isinstance(item, frozenset):
                items = set(item)
                items_to_return = tuple([BaseValue(items.pop()) for _ in range(len(items))])

        elif isinstance(item, BaseContainerTypes().named):
            items_to_return: tuple[BaseValue] = tuple()
            for key, value in item.items():
                items_to_return += (BaseValue(key), BaseValue(value))
            print(items_to_return)

        return items_to_return

    @staticmethod
    def _unpack_container(item: BaseContainerTypes().all, depth: int = 1) -> tuple[BaseValue]:
        """
        Unpacks the container to depth
        """
        unpacked_items: tuple[BaseValue] = tuple()

        if depth >= 1:
            if isinstance(item, BaseValue | BaseValueTypes().all):
                return (item, )

            elif BaseContainer._contains_sub_container(item):
                unpacked_items = unpacked_items + BaseContainer._extract_base_values(item)
                for value in BaseContainer._iter_all_(item):
                    unpacked_items = unpacked_items + BaseContainer._unpack_container(value, depth - 1)

        return unpacked_items

    @staticmethod
    def _iter_all_(item: BaseContainerTypes().all | BaseValueTypes().all):
        """
        Checks if container contains a sub container
        """
        if isinstance(item, BaseValue | BaseValueTypes().all):
            yield item

        elif isinstance(item, BaseContainerTypes().all().linear | BaseContainer):
            for value in item:
                yield BaseContainer._unpack_container(value)

        elif isinstance(item, BaseContainerTypes().all().named):
            for key, value in item.items():
                yield BaseContainer._unpack_container(value)
                yield BaseContainer._unpack_container(key)

    @staticmethod
    def _package(item: BaseContainerTypes().all, type_: TypeAlias | type) -> BaseContainerTypes().all:
        """
        Repackages the container
        """
        match (str(type_)):
            case("<class 'list'>"):
                return [value.value for value in item]
            case("<class 'tuple'>"):
                return tuple([value.value for value in item])
            case("<class 'set'>"):
                return {value.value for value in item}
            case("<class 'frozenset'>"):
                return frozenset({value.value for value in item})
            case("<class 'dict'>"):
                keys: tuple[BaseValueTypes().all] = item[::2]
                values: tuple[BaseValueTypes().all] = item[1::2]
                return {key.value: value.value for key, value in zip(keys, values)}

    # def _package(self) -> BaseValueTypes().all | BaseContainerTypes().all:
    #     return _convert_container_to_default(self._items, self._type)

    def __iter__(self):
        yield from self._items

    def __str__(self) -> str:
        return str(self._package())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={[item for item in iter(self)]}, type={self._type})"
