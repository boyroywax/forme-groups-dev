from ..base.types import BaseContainerTypes, BaseValueTypes
from ..base import BaseValue

from typing import TypeAlias


base_types: TypeAlias = BaseValueTypes().all | BaseContainerTypes().all

def _convert_value_to_type(item: base_types) -> TypeAlias | type:
    print(item)


def _convert_container_to_value(item: base_types) -> BaseValueTypes().all:
    """
    Converts container to value
    """
    item_to_return: BaseValueTypes().all = item
    if isinstance(item, BaseContainerTypes().linear):
        print(Exception("Passed a container, but expected a value, returning the first value of the container"))

        if isinstance(item, list | tuple):
            item_to_return = item[0]

        elif isinstance(item, set):
            item_to_return = item.pop()

        elif isinstance(item, frozenset):
            item_to_return = set(item).pop()

    elif isinstance(item, BaseContainerTypes().named):
        print(Exception("Passed a container, but expected a value, returning the first value of the container"))
        item_to_return = item[list(item.keys())[0]]

    return item_to_return


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

def _convert_container_to_type(item: base_types) -> TypeAlias | type:
    return type(item)

def _convert_container_to_default(item: tuple[BaseContainerTypes().all], type_: TypeAlias | type) -> base_types:
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