from ..base.types import UnitTypes, UnitValueTypes, LinearContainer, NamedContainer, Containers
# from ..base import BaseValue

from typing import TypeAlias


def _convert_value_to_type(item: UnitValueTypes) -> TypeAlias | type:
    return type(item)


def _convert_container_to_value(item: UnitTypes) -> UnitValueTypes:
    """
    Converts container to value
    """
    item_to_return: UnitValueTypes = item
    if isinstance(item, LinearContainer):
        print(Exception("Passed a container, but expected a value, returning the first value of the container"))

        if isinstance(item, list | tuple):
            item_to_return = item[0]

        elif isinstance(item, set):
            item_to_return = item.pop()

        elif isinstance(item, frozenset):
            item_to_return = set(item).pop()

    elif isinstance(item, NamedContainer):
        print(Exception("Passed a container, but expected a value, returning the first value of the container"))
        item_to_return = item[list(item.keys())[0]]

    return item_to_return


# def _convert_container_to_base_values(item: unit_types) -> tuple[BaseValue]:
#     """
#     Converts container to base values
#     """
#     if isinstance(item, linear_container):
#         print(Exception("Passed a container of values, but expected a container of base values, a tuple of BaseValue will be returned"))

#         if isinstance(item, list | tuple):
#             item_to_return = tuple([BaseValue(value) for value in item])

#         elif isinstance(item, set):
#             item_to_return = tuple([BaseValue(item.pop()) for _ in range(len(item))])

#         elif isinstance(item, frozenset):
#             items = set(item)
#             item_to_return = tuple([BaseValue(items.pop()) for _ in range(len(items))])

#     elif isinstance(item, named_container):
#         keys: tuple[unit_value_types] = tuple(item.keys())
#         values: tuple[unit_value_types] = tuple(item.values())
#         item_to_return = tuple([BaseValue(value) for value in itertools.chain(keys, values)])

#     return item_to_return

def _convert_container_to_type(item: UnitTypes) -> TypeAlias | type:
    return type(item)

def _convert_container_to_default(item: tuple[Containers], type_: TypeAlias | type) -> UnitTypes:
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
            keys: tuple[UnitValueTypes] = item[::2]
            values: tuple[UnitValueTypes] = item[1::2]
            return {key.value: value.value for key, value in zip(keys, values)}