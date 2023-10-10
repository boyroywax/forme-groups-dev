"""
BASE INTERFACE

This interface is the base interface for all classes in the project.

NOTES:
    A. SLOTS
        1. __slots__ should not contain a __weakref__ slot.
        2. __slots__ should not contain a __dict__ slot.
        3. Slots should be frozen.
        4. Public Slots should begin with a lowercase letter.
        4. Private Slots should be prefixed with an underscore ("_").
    B. REPRESENTATION
        1. __repr should include all slots (including private slots).
    C. STRING DUNDER METHOD
        1. __str__ should include only public slots.
    D. HASHING
        1. Hashing a Base Item into a leaf




"""

from abc import ABC
from attrs import define

from ..utils.crypto import MerkleTree


@define(frozen=True, slots=True, weakref_slot=False)
class BaseInterface(ABC):
    """
    Base interface for all classes
    """
    def __iter__slots__(self, include_underscored_slots: bool = False, private_only: bool = False):
        """Returns an iterator over all slots."""
        if not include_underscored_slots and private_only:
            raise ValueError("Cannot exclude underscored slots and only include private slots.  Private slots are prefixed with an underscore (\"_\").")

        for slot in self.__slots__:
            if private_only:
                if slot.startswith("_"):
                    yield slot
            else:
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
        yield from self.__iter__slots__(include_underscored_slots=True, private_only=False)

    def __repr_private__(self, include_underscored_slots: bool = True, private_only: bool = False) -> str:
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
        return f"{self.__class__.__name__}({', '.join([f'{slot}={getattr(self, slot)}' for slot in self.__iter__slots__(include_underscored_slots=include_underscored_slots, private_only=private_only)])})"

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

    def __str_item__(self, item: str) -> str:
        """Returns a string of a slot and its value.

        Returns:
            str: A string containing a slot and its value.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().__str_item__("test_property")
            'test_property: 1'
        """
        return f"{item}: {getattr(self, item)}"

    def __str_private__(self, include_underscored_slots: bool = True, private_only: bool = False) -> str:
        """Returns a string of key-value pairs of slots and their values.

        Returns:
            str: A string containing both public and private slots and their values.

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
        for slot in self.__iter__slots__(include_underscored_slots, private_only):
            slot_string += f"{self.__str_item__(slot)}, "

        return slot_string[:-2] if len(slot_string) > 0 else slot_string

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
        return self.__str_private__(include_underscored_slots=False, private_only=False)

    def _hash_leaf(self, include_underscored_slots: bool = True) -> str:
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
        return MerkleTree.hash_func(self.__repr_private__(include_underscored_slots, private_only=False))

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
        for slot in self.__iter__slots__(include_underscored_slots=True, private_only=False):
            hashed_slots.append(MerkleTree.hash_func(getattr(self, slot)))

        return MerkleTree(hashed_slots)
