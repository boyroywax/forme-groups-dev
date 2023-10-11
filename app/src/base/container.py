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


def _base_container_type_validator(instance, attribute, value):
    """Validates the argument is a BaseContainerTypes

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        GroupBaseContainerException: If the value is not a BaseContainerTypes
    """
    base_container_types = BaseContainerTypes()
    if isinstance(value, str):
        if base_container_types._get_type_from_alias(value) is None:
            raise GroupBaseContainerException(f"Expected a container, but received {value}")
    # elif isinstance(value, type):
    #     print(value)
    #     if base_container_types._verify_base_container_type(value.__name__) is False:
    #             raise GroupBaseContainerException(f"Expected a container, but received {value}")
    elif isinstance(value, BaseContainerTypes().all):
        if len(value) > 0:
            raise GroupBaseContainerException(f"Expected a container, but received {value}")


def _base_container_type_converter(item: BaseContainerTypes().all) -> BaseContainerTypes().all:
    """
    Converter function for _type field
    """
    base_container_types = BaseContainerTypes()
    type_from_alias: TypeAlias | type = None
    if isinstance(item, str):
        type_from_alias = base_container_types._get_type_from_alias(item)
        if type_from_alias is None:
            raise GroupBaseContainerException(f"Expected a container, but received {type(item)}")
    elif isinstance(item, type):
        type_from_alias = item

    return type_from_alias


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainer[T: BaseContainerTypes().all](BaseInterface):

    _items: tuple[BaseValue] = field(
        validator=validators.deep_iterable(validators.instance_of(BaseValue), iterable_validator=validators.instance_of(tuple)),
        converter=_base_container_converter
    )
    _type: Optional[Type[BaseContainerTypes().all]] = field(
        # validator=validators.instance_of(type |  str),
        validator=_base_container_type_validator,
        converter=_base_container_type_converter,
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
        return self._type.__name__
    
    @staticmethod
    def _iter_all_(item: BaseContainerTypes().all | BaseValueTypes().all | BaseValue):
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
        base_container_types = BaseContainerTypes()
        type_from_alias: TypeAlias | type = base_container_types._get_type_from_alias(type_)
        match (str(type_from_alias)):
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

    @override
    def __repr__(self) -> str:
        return f"BaseContainer(items={self.items}, type={self.type})"

    @override
    def __str__(self) -> str:
        return str(self._package(item=self.items, type_=self.type))

    @override
    def __iter__(self):
        return iter(self.items)
