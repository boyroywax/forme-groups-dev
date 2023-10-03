from abc import ABCMeta, abstractmethod, ABC
from attrs import define, field, validators, converters
from typing import TypeAlias, Optional


number: TypeAlias = int | float
text: TypeAlias = str | bytes
container: TypeAlias = list | tuple | dict | set | frozenset
object_: TypeAlias = object | None
unit_types: TypeAlias = number | text | container | object_


@define(frozen=True, slots=True,  weakref_slot=False)
class BaseInterface[T: unit_types](ABC):
    """
    A value object.
    """

    _value: Optional[unit_types] = field(default=None, validator=validators.optional(validators.instance_of(unit_types)))

    def _is_type(self) -> TypeAlias:
        """
        Returns True if the value is of the type specified by the class.
        """
        if isinstance(self._value, number):
            return number

        if isinstance(self._value, text):
            return text

        if isinstance(self._value, container):
            return container

        if isinstance(self._value, object_):
            return object_

    def _slots_to_string(
        self,
        values_only: Optional[bool] = True,
        keys_only: Optional[bool] = False,
        exclude: Optional[list] = None,
    ) -> str:
        """
        Returns a string representation of the object's slots.
        """
        assert values_only is not True or keys_only is not True, (
            "values_only and keys_only cannot both be True")

        if exclude is None:
            exclude = []

        slots = self.__slots__
        _slot_str: str = ""
        for slot in slots:
            if slot not in exclude:
                value = getattr(self, slot)
                if keys_only:
                    _slot_str += f'{slot}, '
                elif values_only:
                    _slot_str += f'{value}, '
                else:
                    _slot_str += f"{slot}={value}, "
        return _slot_str[:-2]

    def __str__(self) -> str:
        return self._slots_to_string()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._slots_to_string(values_only=False)})"
    
    def _contains_sublevel(self, data) -> bool:
        """
        Returns True if the data contains a sublevel.
        """
        if isinstance(data, container):
            return True
        else:
            return False

    def _get_sublevel(self, data=None) -> list[T]:
        sublevel_value = []
        if self._contains_sublevel(data):
            for item in data:
                sublevel_value.append(item)
        return sublevel_value
        
    def _map_sublevel(self, data = None) -> list[T]:
        """
        Returns a list of the sublevels of the data.
        """
        sublevels = []
        if data is None:
            for slot in self.__slots__:
                data = getattr(self, slot)
                break

        for item in self._list_items_with_sublevels(data):
            sublevels.append(self._get_sublevel(data[item]))
        
        return sublevels

    def _list_items_with_sublevels(self, data=None) -> list[T]:
        """
        Returns a list of the items with sublevels.
        """
        items_with_sublevels = []
        if data is None:
            for slot in self.__slots__:
                data = getattr(self, slot)
                break

        if self._contains_sublevel(data):
            if isinstance(data, (list, tuple, set, frozenset)):
                for item in data:
                    if self._contains_sublevel(item):
                        items_with_sublevels.append(item)
            elif isinstance(data, dict):
                for key, value in data.items():
                    if self._contains_sublevel(value):
                        items_with_sublevels.append(key)

        return items_with_sublevels



    def _get_max_sublevel(self, data=None, levels: list[int] = [], level: int = 0) -> int:
        """
        Returns the max sublevel of the data.
        """
        if data is None:
            for slot in self.__slots__:
                data = getattr(self, slot)
                break

        if level is None:
            level = 0

        if self._contains_sublevel(data):
            if isinstance(data, (list, tuple, set, frozenset)):
                for item in data:
                    levels.append(self._get_max_sublevel(item, level=level + 1))

            elif isinstance(data, dict):
                for key, value in data.items():
                    levels.append(self._get_max_sublevel(value, level=level + 1))

        else:
            levels.append(level)
        return max(levels)

    def _unpack_container(self, container_: Optional[container] = None, level: Optional[int] = 0):
        # assert isinstance(container_, container), (
            # "container_ must be a container type")
        
        if not isinstance(container_, container):
            return

        if level == 0:
            yield container_

        if level >= 0:
            if isinstance(container_, (list, tuple, set, frozenset)):
                for item in container_:
                    if isinstance(item, container):
                        yield from self._unpack_container(item, level=level-1)
                    else:
                        yield item
            else:
                for key, value in container_.items():
                    if isinstance(value, container):
                        yield (key, value)
                        yield from self._unpack_container(value, level=level-1)
                    else:
                        yield (key, value)

    def __iter__(self):
        """

        """
        level = self._get_max_sublevel()
        for slot in self.__slots__:
            if isinstance(getattr(self, slot), container):
                yield from self._unpack_container(getattr(self, slot), level=level)
            else:
                yield getattr(self, slot)

    def iter_to_depth(self, level: int = 0):
        """
        Returns an iterator to the specified depth.
        """
        assert isinstance(level, int), (
            "level must be an integer")

        for slot in self.__slots__:
            if isinstance(getattr(self, slot), container):
                yield from self._unpack_container(getattr(self, slot), level=level)
            else:
                yield getattr(self, slot)