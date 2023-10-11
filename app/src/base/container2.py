from attrs import define, field, validators
from typing import Optional, TypeAlias, TypeVar, Optional, Type, TypeGuard, override


from .interface import BaseInterface
from .types import BaseValueTypes, BaseContainerTypes
from .value import BaseValue
from .exceptions import GroupBaseContainerException


def _base_container_converter(item: BaseContainerTypes().all) -> tuple[BaseValue]:
    """
    Converter function for _items field
    """
    base_values: tuple = tuple()
    exc_message = f"Expected a non-container, but received {type(item)}"
    # __UNIT__ = type(item)

    if isinstance(item, BaseContainerTypes().linear):
        for item_ in item:
            if isinstance(item_, BaseContainerTypes().all):
                raise GroupBaseContainerException(exc_message)
            
            if isinstance(item_, BaseValue):
                base_values += tuple([item_], )
            else:
                base_values += tuple([BaseValue(item_)])

    elif isinstance(item, BaseContainerTypes().named):
        for key, value in item.items():
            if isinstance(value, BaseContainerTypes().all):
                raise GroupBaseContainerException(exc_message)

            if isinstance(value, BaseValue):
                base_values += tuple([BaseValue(key), value])
            else:
                base_values += tuple([BaseValue(key), BaseValue(value)])
    else:
        raise GroupBaseContainerException(f"Expected a container, but received a non-container {type(item)}")
    
    return base_values


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainer[T: BaseContainerTypes().all](BaseInterface):

    _items: tuple[BaseValue] = field(
        validator=validators.deep_iterable(validators.instance_of(BaseValue)),
        converter=_base_container_converter
    )
    _type: Optional[Type[BaseContainerTypes().all]] = field(
        validator=validators.instance_of(type |  str),
        default=tuple
    )

    @property
    def items(self) -> tuple[BaseValue]:
        """The items held by the BaseContainer Class

        Returns:
            tuple[BaseValue]: The items held by the BaseContainer Class

        Examples:
            >>> container = BaseContainer((1, 2, 3))
            >>> container.items
            (BaseValue(value=1, type=int), BaseValue(value=2, type=int), BaseValue(value=3, type=int))
        """
        return self._items

    @property
    def type(self) -> Type[BaseContainerTypes().all]:
        """The type of the BaseContainer

        Returns:
            Type[BaseContainerTypes]: The type of the BaseContainer

        Examples:
            >>> container = BaseContainer((1, 2, 3))
            >>> container.type
            tuple
        """
        return self._type
    
    @override
    def __repr__(self) -> str:
        return f"BaseContainer(items={self.items}, type={self.type})"
    
    @override
    def __str__(self) -> str:
        return f"{tuple([item.value for item in self.items])}"

    @override
    def __iter__(self):
        return iter(self.items)

