from attrs import define, field, validators
from typing import Optional, TypeAlias, Type, override

from .interface import BaseInterface
from .types import BaseTypes, BaseValueTypes, BaseContainerTypes, LinearContainer, NamedContainer
from .value import BaseValue
from .exceptions import GroupBaseContainerException
from ..utils.crypto import MerkleTree
from ..utils.checks import contains_sub_container, is_linear_container, is_named_container, is_base_container_type


def _base_container_type_converter(item: BaseContainerTypes | str | type) -> BaseContainerTypes:
    """
    Converter function for _type field
    """
    type_from_alias: TypeAlias | type = None
    if isinstance(item, str) and len(item) > 0:
        type_from_alias = BaseTypes._get_type_from_alias(item)

    if type_from_alias is None or isinstance(type_from_alias(), BaseValueTypes):
        raise GroupBaseContainerException(f"Expected a container type, but received {item}")
    elif isinstance(item, BaseContainerTypes):
        type_from_alias = type(item)

    return type_from_alias


def _base_container_converter(item: BaseContainerTypes) -> tuple[BaseValue]:
    """
    Converter function for _items field
    """
    base_values: tuple = tuple()
    exc_message = f"Expected a non-container, but received {type(item)}"

    if contains_sub_container(item):
        raise GroupBaseContainerException(exc_message)

    if is_linear_container(item):
        for item_ in item:
            if is_base_container_type(item_):
                raise GroupBaseContainerException(exc_message)

            if isinstance(item_, BaseValue):
                base_values += tuple([item_], )
            else:
                base_values += tuple([BaseValue(item_)])

    elif is_named_container(item):
        for key, value in item.items():
            if is_base_container_type(key) or is_base_container_type(value):
                raise GroupBaseContainerException(exc_message)

            if isinstance(value, BaseValue):
                base_values += tuple([BaseValue(key), value])
            else:
                base_values += tuple([BaseValue(key), BaseValue(value)])
    else:
        raise GroupBaseContainerException(f"Expected a container, but received a non-container {type(item)}")

    return base_values


@define(frozen=True, slots=True, weakref_slot=False)
class BaseContainer(BaseInterface):
    """The BaseContainer class holds Base Values

    Args:
        items (tuple[BaseValue]): The items held by the BaseContainer Class
        type (Type[BaseContainerTypes | str]): The type of the BaseContainer

    Examples:
        >>> container = BaseContainer((1, 2, 3))
        >>> container
        BaseContainer(items=(BaseValue(value=1, type=int), BaseValue(value=2, type=int), BaseValue(value=3, type=int)), type=tuple)
    """

    _items: tuple[BaseValue] = field(
        validator=validators.deep_iterable(validators.instance_of(BaseValue | BaseValueTypes),
        iterable_validator=validators.instance_of(tuple)),
        converter=_base_container_converter
    )
    _type: Optional[Type[BaseContainerTypes] | str] = field(
        validator=validators.instance_of(type | str),
        converter=_base_container_type_converter,
        default="tuple"
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
    def type(self) -> Type[BaseContainerTypes | str]:
        """The type of the BaseContainer

        Returns:
            Type[BaseContainerTypes]: The type of the BaseContainer

        Examples:
            >>> container = BaseContainer((1, 2, 3))
            >>> container.type
            tuple
        """
        return self._type.__name__ if isinstance(self._type, type) else self._type

    @staticmethod
    def _unpack(item: BaseContainerTypes, type_: TypeAlias | type) -> BaseContainerTypes:
        """
        Repackages the container
        """
        type_from_alias: TypeAlias | type = BaseTypes._get_type_from_alias(type_)
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
                keys: tuple[BaseValue] = item[::2]
                values: tuple[BaseValue] = item[1::2]
                return {key.value: value.value for key, value in zip(keys, values)}
            case _:
                raise GroupBaseContainerException(f"Expected a container, but received {type_}")

    @override
    def __repr__(self) -> str:
        return f"BaseContainer(items={self.items}, type={self.type})"

    @override
    def __str__(self) -> str:
        return str(self._unpack(item=self.items, type_=self.type))

    def __iter_items__(self, slot_name: str = "_items"):
        """Returns an iterator over all slots.

        Returns:
            Iterator[str]: An iterator over all slots.
        """
        items: tuple = getattr(self, slot_name)

        # if isinstance(items, BaseValue | BaseValueTypes):
        #     yield items

        if isinstance(items, LinearContainer | BaseContainer):
            for value in items:
                yield value

        elif isinstance(items, NamedContainer):
            for key, value in items.items():
                yield value
                yield key

    @override
    def __iter__(self):
        yield from self.__iter_items__()

    def _hash_type(self) -> str:
        return MerkleTree._hash_func(self.type)

    def _hash_items(self) -> MerkleTree:
        hashed_items: tuple[str, ...] = ()
        for item in self.__iter_items__():
            hashed_items = hashed_items + (item._hash().root(), )

        return MerkleTree(hashed_items)

    def _hash(self) -> MerkleTree:
        return MerkleTree((self._hash_type(), self._hash_items().root(), ))

    def _verify_item(self, item: BaseValue) -> bool:
        assert isinstance(item, BaseValue), f"Expected a BaseValue, but received {type(item)}"

        leaf_hash: str | None = item._hash().root()
        tree = self._hash_items()

        return tree.verify(leaf_hash)