"""
BASE INTERFACE

This interface is the base interface for all classes in the project.

NOTES:
    A. SLOTS DUNDER METHOD
        1. __slots__ should not contain a __weakref__ slot.
        2. __slots__ should not contain a __dict__ slot.
        3. Slots should be frozen.
        4. Slots are named in two ways:
            a. Public Slots -> begin with a lowercase letter.
            b. Private Slots -> prefixed with an underscore ("_").

    B. ITERATION DUNDER METHOD
        1. __iter__ should iterate over all slots (including private slots).
        2. __iter_slots__ can return an iterator over:
            a. only public slots or
            b. only private slots or
            c. both
        3. __iter_slots__ will not unpack the slots if it contains a tuple, list, dict, or set.
        4. By default, __iter__ calls __iter_slots__().
            a. An Example with default include_underscored_slots=True and private_only=False:
                >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
                >>> from attrs import define
                >>> @define(frozen=True, slots=True, weakref_slot=False)
                ... class BaseInterfaceExample(BaseInterface):
                ...     test_property: int = 1
                ...     _private_test_property: int = 2
                >>> list(BaseInterfaceExample())
                ['test_property', '_private_test_property']

    C. REPRESENTATION DUNDER METHOD
        1. __repr__ should include the repr() of all slots (including private slots).
        2. __repr_private__ can return a string representation of the object with:
            a. only public slots or
            b. only private slots or
            c. both
        3. By default, __repr__ calls __repr_private__().
            a. An Example with default include_underscored_slots=True and private_only=False:
                >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
                >>> from attrs import define
                >>> @define(frozen=True, slots=True, weakref_slot=False)
                ... class BaseInterfaceExample(BaseInterface):
                ...     test_property: int = 1
                ...     _private_test_property: int = 2
                >>> BaseInterfaceExample().__repr__()
                'BaseInterfaceExample(test_property=1, _private_test_property=2)'

    D. STRING DUNDER METHOD
        1. __str__ should include only public slots.
        2. __str_private__ can return a string representation of the object with:
            a. only public slots or
            b. only private slots or
            c. both
        3. By default, __str__ calls __str_private__().
        4. In turn, __str_private__() calls __str_item__() for each slot, which returns a string of the slot and its value.
            a. An Example with default include_underscored_slots=True and private_only=False:
                >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
                >>> from attrs import define
                >>> @define(frozen=True, slots=True, weakref_slot=False)
                ... class BaseInterfaceExample(BaseInterface):
                ...     test_property: int = 1
                ...     _private_test_property: int = 2
                >>> BaseInterfaceExample().__str__()
                'test_property: 1, _private_test_property: 2'

    E. HASHING
        1. The __hash__ dunder method is not used. (__hash__() expects a type int to be returned)
        2. Hashing a Base Class Representation
            a. Hashes the full representation of the object including private slots.
            b. If a __repr__ is overridden in a subclass, the new __repr__ will be used to hash the object.
            c. Can only be used to verify the full representational string of the object.
            d. An Example with an overridden __repr__:
                >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
                >>> from attrs import define
                ... class BaseInterfaceExample(BaseInterface):
                ...     @override
                ...     def __repr__(self) -> str:
                ...         return "test"
                >>> BaseInterfaceExample().hash_repr()
                'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
        3. Hashing a Base Class into a Tree
            a. Hashes each slot's representation by calling the __repr__ of each slot.
            b. Then, the slot hashes are hashed into a tree.
            c. Can be used to verify the findividual slots of the object.
            d. An Example with default include_underscored_slots=True and private_only=False:
                >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
                >>> from attrs import define
                ... class BaseInterfaceExample(BaseInterface):
                ...     test_property: int = 1
                ...     _private_test_property: int = 2
                >>> BaseInterfaceExample().hash_slots()
                ('b4c5b6872918d107cff29a9b6a0c81e7c2c450dd46285055beb0deefefa04271', 'b4c5b6872918d107cff29a9b6a0c81e7c2c450dd46285055beb0deefefa04271')
        4. Hashing a Base Class into a Package
            a. Hashes each public slot into a leaf.
            b. Then, hashes the public leaves into a tree.
            c. Next, each private slot is hashed into a leaf.
            d. Then, hashes the private leaves into a tree.
            e. Finally, the public and private trees are hashed together into a tree representing the package.

"""

from abc import ABC
from attrs import define

from .exceptions import GroupBaseException
from ..utils.crypto import MerkleTree


@define(frozen=True, slots=True, weakref_slot=False)
class BaseInterface(ABC):
    """
    Base interface for all classes
    """

    def __iter_slots__(self, include_underscored_slots: bool = False, private_only: bool = False):
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
        """
        yield from self.__iter_slots__(include_underscored_slots=True, private_only=False)

    def __repr_private__(self, include_underscored_slots: bool = True, private_only: bool = False) -> str:
        """Returns a string representation of the object in a standard format.

        NOTE: All slots are included in the string representation (including private slots).

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
        return f"{self.__class__.__name__}({', '.join([f'{slot}={repr(getattr(self, slot))}' for slot in self.__iter_slots__(include_underscored_slots, private_only)])})"

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
        return self.__repr_private__(include_underscored_slots=True, private_only=False)

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
            ...     _private_test_property: int = 2
            >>> BaseInterfaceExample().__str_private__()
            'test_property: 1, _private_test_property: 2'
        """
        slot_string: str = ""
        for slot in self.__iter_slots__(include_underscored_slots, private_only):
            slot_string += f"{self.__str_item__(slot)}, "

        return slot_string[:-2] if len(slot_string) > 0 else slot_string

    def __str__(self) -> str:
        """Returns a string of key-value pairs of slots and their values.

        NOTE: Slots starting with an underscore ("_") are ignored.

        Returns:
            str: A string containing slots and their values.

        """
        return self.__str_private__(include_underscored_slots=False, private_only=False)
    
    def _hash_repr(self) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        """
        return MerkleTree._hash_func(repr(self))

    def _hash_slot(self, slot: str) -> str:
        """Returns the sha256 hash of the representation of the value of a slot in the object.

        """
        return MerkleTree._hash_func(repr(getattr(self, slot)))

    def _hash_slots(self, include_underscored_slots: bool = True, private_only: bool = False) -> tuple[str]:
        """Returns the sha256 hash of the representation of each slot in the object.

        Returns:
            str: The hash of the representation of the object.

        """
        hashed_slots: tuple[str] = ()
        for slot in self.__iter_slots__(include_underscored_slots, private_only):
            hashed_slots = hashed_slots + (self._hash_slot(slot), )

        return hashed_slots

    def _hash_tree(self, include_underscored_slots: bool = True, private_only: bool = False) -> MerkleTree:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        """
        return MerkleTree(self._hash_slots(include_underscored_slots, private_only))

    def _hash_public_slots(self) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        """
        return self._hash_tree(include_underscored_slots=False, private_only=False).root()

    def _hash_private_slots(self) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        """
        return self._hash_tree(include_underscored_slots=True, private_only=True).root()
    
    def _check_for_none(self, item: str) -> bool:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        """
        return item is None

    def _hash_package(self) -> MerkleTree:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        """
        public_hash: str | None = self._hash_public_slots()
        private_hash: str | None = self._hash_private_slots()

        if self._check_for_none(public_hash) and self._check_for_none(private_hash):
            raise GroupBaseException("Cannot hash a package with no public or private slots.")
        
        merkle_tree = None

        if self._check_for_none(public_hash) and not self._check_for_none(private_hash):
            merkle_tree = MerkleTree(hashed_data=(private_hash, ))
        elif self._check_for_none(private_hash) and not self._check_for_none(public_hash):
            merkle_tree = MerkleTree(hashed_data=(public_hash, ))
        elif not self._check_for_none(public_hash) and not self._check_for_none(private_hash):
            merkle_tree = MerkleTree(hashed_data=(public_hash, private_hash))

        return merkle_tree

    def _verify_item_in_hash_package(self, item: str) -> bool:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        """
        leaf_hash: str = MerkleTree._hash_func(repr(getattr(self, item)))
        public_tree = self._hash_public_slots()
        private_tree = self._hash_private_slots()

        return public_tree.verify(leaf_hash) or private_tree.verify(leaf_hash)