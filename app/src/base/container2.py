# from attrs import define, field, validators
# from typing import Optional, TypeAlias, TypeVar, Optional, Type, TypeGuard


# from .interface import BaseInterface
# from .types import BaseValueTypes, BaseContainerTypes
# from .value import BaseValue
# from .exceptions import GroupBaseContainerException


# def is_named_container(item: object) -> TypeGuard[dict]:
#     """
#     Type guard for named containers
#     """
#     return isinstance(item, dict)


# def is_unnamed_container(item: object) -> TypeGuard[Type[BaseContainerTypes().all]]:
#     """
#     Type guard for unnamed containers
#     """
#     return isinstance(item, BaseContainerTypes().all)


# def _base_container_converter(item: object) -> tuple[BaseValue]:
#     """
#     Converter function for _items field
#     """
#     exc_message = f"Invalid container type: {type(item)}"

#     if is_unnamed_container(item):
#         for item_ in item:
#             if isinstance(item_, BaseContainerTypes().all):
#                 raise GroupBaseContainerException(exc_message)

#         base_values = tuple(BaseValue(item_) for item_ in item)

#     elif is_named_container(item):
#         for key, value in item.items():
#             if isinstance(value, BaseContainerTypes().all):
#                 raise GroupBaseContainerException(exc_message)

#         base_values = tuple(BaseValue(key) for key in item.keys()) + tuple(BaseValue(value) for value in item.values())

#     else:
#         raise GroupBaseContainerException(f"Expected a container, but received a non-container {type(item)}")

#     return base_values


# @define(frozen=True, slots=True, weakref_slot=False)
# class BaseContainer(BaseInterface):

#     _items: tuple[BaseValue] = field(
#         validator=validators.deep_iterable(validators.instance_of(BaseValue), iterable_validator=is_unnamed_container),
#         converter=_base_container_converter
#     )
#     _type_alias: Type[BaseContainerTypes().all] = field(
#         validator=validators.instance_of(Type[BaseContainerTypes().all]),
#         type_guard=is_unnamed_container
#     )

#     @property
#     def items(self) -> tuple[BaseValue]:
#         """The items held by the BaseContainer Class

#         Returns:
#             tuple[BaseValue]: The items held by the BaseContainer Class

#         Examples:
#             >>> container = BaseContainer((1, 2, 3))
#             >>> container.items
#             (BaseValue(value=1, type=int), BaseValue(value=2, type=int), BaseValue(value=3, type=int))
#         """
#         return self._items

#     @property
#     def type(self) -> Type[BaseContainerTypes().all]:
#         """The type of the BaseContainer

#         Returns:
#             Type[BaseContainerTypes]: The type of the BaseContainer

#         Examples:
#             >>> container = BaseContainer((1, 2, 3))
#             >>> container.type
#             tuple
#         """
#         return self._type_alias

# # def _base_container_converter(item: BaseContainerTypes().all) -> tuple[BaseValue]:
# #     """The converter for BaseContainer

# #     Args:
# #         value (tuple[BaseValue]): The value to convert

# #     Returns:
# #         tuple[BaseValue]: The converted value
# #     """
# #     base_values: tuple = tuple()
# #     exc_message = f"Expected a non-container, but received {type(item)}"

# #     if isinstance(item, BaseContainerTypes().linear):
# #         for item_ in item:
# #             if isinstance(item_, BaseContainerTypes().all):
# #                 raise GroupBaseContainerException(exc_message)
            
# #             if isinstance(item_, BaseValue):
# #                 base_values += tuple([item_], )
# #             else:
# #                 base_values += tuple([BaseValue(item_)])

# #     elif isinstance(item, BaseContainerTypes().named):
# #         for key, value in item.items():
# #             if isinstance(value, BaseContainerTypes().all):
# #                 raise GroupBaseContainerException(exc_message)

# #             if isinstance(value, BaseValue):
# #                 base_values += tuple([BaseValue(key), value])
# #             else:
# #                 base_values += tuple([BaseValue(key), BaseValue(value)])
# #     else:
# #         raise GroupBaseContainerException(f"Expected a container, but received a non-container {type(item)}")
    
# #     return base_values


# # @define(frozen=True, slots=True, weakref_slot=False)
# # class BaseContainer[T: BaseContainerTypes().all](BaseInterface):

# #     _items: tuple[BaseValue] = field(
# #         # validator=validators.deep_iterable(validators.instance_of(BaseValue), iterable_validator=validators.instance_of(BaseContainerTypes().all)),
# #         # converter=_base_container_converter,
# #         # init=False
# #     )
# #     _type_alias: Optional[BaseContainerTypes().all | str] = field(
# #         validator=validators.optional(validators.instance_of(BaseContainerTypes().all | str)),
# #         # default=type(_items),
# #         init=False
# #     )

# #     def __pre_init__(self, *args, **kwargs):
# #         """Pre-initializer for BaseContainer

# #         Args:
# #             items (T): The items to hold
# #         """
# #         items: T = kwargs.get("_items", None) if len(args) == 0 else args[0]
# #         type_alias: Optional[BaseContainerTypes().all | str] = kwargs.get("_type_alias", None) if len(args) == 1 else args[1]

# #         # if type_alias is not None:
# #         self._type_alias = items
# #         # elif isinstance(items, BaseContainerTypes().all):
# #             # self._type_alias = type(items)

# #         # if isinstance(items, BaseContainerTypes().all):
# #         self._items = _base_container_converter(items)
# #         # else:
# #             # raise GroupBaseContainerException(f"Expected a container, but received {type(items)}")
        
# #         # self.__init__(items=self._items)


# #     @property
# #     def items(self) -> tuple[BaseValue]:
# #         """The items held by the BaseContainer Class

# #         Returns:
# #             tuple[BaseValue]: The items held by the BaseContainer Class

# #         Examples:
# #             >>> container = BaseContainer((1, 2, 3))
# #             >>> container.items
# #             (BaseValue(value=1, type=int), BaseValue(value=2, type=int), BaseValue(value=3, type=int))
# #         """
# #         return self._items
    
# #     @property
# #     def type(self) -> BaseContainerTypes().all:
# #         """The type of the BaseContainer

# #         Returns:
# #             BaseContainerTypes: The type of the BaseContainer

# #         Examples:
# #             >>> container = BaseContainer((1, 2, 3))
# #             >>> container.type
# #             tuple
# #         """
# #         return self._type_alias


