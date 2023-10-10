"""
BASE INTERFACE

This interface is the base interface for all classes in the project.



__str__() returns a string representation of the object.
* The string is a comma-separated list of all slots and their values.
>>> # __str__() example





"""

from abc import ABC
from attrs import define

from ..utils.crypto import MerkleTree


@define(frozen=True, slots=True, weakref_slot=False)
class BaseInterface(ABC):
    """
    Base interface for all classes
    """
    def _get_slots(self, include_underscored_slots: bool = False):
        """Returns an iterator over all slots."""
        for slot in self.__slots__:
            if not include_underscored_slots and slot.startswith("_"):
                continue
            else:
                yield slot

    def __iter__(self):
        """Returns an iterator over all slots.
        
        Returns:
            Iterator[str]: An iterator over all slots.
            
            Example:
                >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
                >>> from attrs import define
                >>> @define(frozen=True, slots=True, weakref_slot=False)
                ... class BaseInterfaceExample(BaseInterface):
                ...     test_property: int = 1
                >>> list(BaseInterfaceExample())
                ['test_property']
        """
        yield from self._get_slots(include_underscored_slots=True)

    def __repr_private__(self, include_underscored_slots: bool = True) -> str:
        """Returns a string representation of the object in a standard format.

        NOTE: All slots are included in the string representation.

        Returns:
            str: A string representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().__repr__()
            'BaseInterfaceExample(test_property=1)'
        """
        return f"{self.__class__.__name__}({', '.join([f'{slot}={getattr(self, slot)}' for slot in self._get_slots(include_underscored_slots=include_underscored_slots)])})"

    def __repr__(self) -> str:
        """Returns a string representation of the object in a standard format.

        NOTE: All slots are included in the string representation.

        Returns:
            str: A string representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().__repr__()
            'BaseInterfaceExample(test_property=1)'
        """
        return self.__repr_private__(include_underscored_slots=True)

    def __str__(self) -> str:
        """Returns a string of key-value pairs of slots and their values.

        NOTE: Slots starting with an underscore ("_") are ignored.

        Returns:
            str: A string containing slots and their values.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().__str__()
            'test_property: 1'
        """
        slot_string: str = ""
        for slot in self._get_slots(include_underscored_slots=False):
            slot_string += f'{slot}: {getattr(self, slot)}, '
        return slot_string[:-2] if len(slot_string) > 0 else slot_string

    def _hash_leaf(self, include_underscored_slots: bool = False) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().hash_leaf()
            '1f5cea5f9f2e15a85423063b80d372f4707d46a3c849d94ef2e7dd0c672daa17'
        """
        return MerkleTree.hash_func(self.__repr_private__(include_underscored_slots))
    
    def _hash_tree(self) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().hash_tree()
            '1f5cea5f9f2e15a85423063b80d372f4707d46a3c849d94ef2e7dd0c672daa17'
        """
        hashed_slots: list[str] = []
        for slot in self._get_slots(include_underscored_slots=True):
            hashed_slots.append(MerkleTree.hash_func(getattr(self, slot)))

        return MerkleTree(hashed_slots)
