from ..base.types import BaseContainerTypes, BaseValueTypes
from ..base import BaseValue

from typing import TypeAlias
from ..base.types import AllBaseContainerTypes, AllBaseValueTypes, BaseTypes
from ..base.exceptions import GroupBaseContainerException
from .checks import _contains_sub_container, is_linear_container, is_named_container


base_types  = BaseTypes


def _base_type_converter(item: str | int | float | bytes | dict | list| tuple | set | frozenset |type) -> TypeAlias | type:
    """
    Converter function for _value field
    """
    base_container_types = BaseContainerTypes()
    base_value_types = BaseValueTypes()
    type_from_alias: TypeAlias | type = None
    if isinstance(item, str) and len(item) > 0:
        type_from_value_alias = base_value_types._get_type_from_alias(item)
        type_from_container_alias = base_container_types._get_type_from_alias(item)
        assert type_from_value_alias is not None or type_from_container_alias is not None, f"Expected a type, but received {item}"
        type_from_alias = type_from_value_alias if type_from_value_alias is not None else type_from_container_alias
    elif isinstance(item, type):
        type_from_alias = item
    elif isinstance(item, (int, float, bytes, dict, list, tuple, set, frozenset)):
        type_from_alias = type(item)

    return type_from_alias


def _base_container_type_converter(item: AllBaseContainerTypes | str) -> AllBaseContainerTypes:
    """
    Converter function for _type field
    """
    base_container_types = BaseContainerTypes()
    type_from_alias: TypeAlias | type = None
    if isinstance(item, str) and len(item) > 0:
        type_from_alias = base_container_types._get_type_from_alias(item)
    elif isinstance(item, type):
        type_from_alias = item

    return type_from_alias


def _base_container_converter(item: AllBaseContainerTypes) -> tuple[BaseValue]:
    """
    Converter function for _items field
    """
    base_values: tuple = tuple()
    exc_message = f"Expected a non-container, but received {type(item)}"
    # __UNIT__ = type(item)

    if _contains_sub_container(item):
        raise GroupBaseContainerException(exc_message)

    if is_linear_container(item):
        for item_ in item:
            if isinstance(item_, AllBaseContainerTypes):
                raise GroupBaseContainerException(exc_message)
            
            if isinstance(item_, BaseValue):
                base_values += tuple([item_], )
            else:
                base_values += tuple([BaseValue(item_)])

    elif is_named_container(item):
        for key, value in item.items():
            if isinstance(value, AllBaseContainerTypes):
                raise GroupBaseContainerException(exc_message)

            if isinstance(value, BaseValue):
                base_values += tuple([BaseValue(key), value])
            else:
                base_values += tuple([BaseValue(key), BaseValue(value)])
    else:
        raise GroupBaseContainerException(f"Expected a container, but received a non-container {type(item)}")
    
    return base_values

def _convert_value_to_type(item: base_types) -> TypeAlias | type:
    print(item)


def _convert_container_to_value(item: base_types) -> BaseValueTypes:
    """
    Converts container to value
    """
    item_to_return: BaseValueTypes = item
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


def _extract_base_values(item: BaseContainerTypes) -> tuple[BaseValue]:
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


def _convert_container_to_default(item: tuple[BaseContainerTypes], type_: TypeAlias | type) -> base_types:
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
            keys: tuple[BaseValueTypes] = item[::2]
            values: tuple[BaseValueTypes] = item[1::2]
            return {key.value: value.value for key, value in zip(keys, values)}