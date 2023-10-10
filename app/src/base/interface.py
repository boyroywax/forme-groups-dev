"""
BASE INTERFACE

This interface is the base interface for all classes in the project.

NOTES:
    A. SLOTS DUNDER METHOD
        1. __slots__ should not contain a __weakref__ slot.
        2. __slots__ should not contain a __dict__ slot.
        3. Slots should be frozen.
        4. Slots are named in two ways:
            a. Public Slots -> should begin with a lowercase letter.
            b. Private Slots -> should be prefixed with an underscore ("_").
    B. ITERATION DUNDER METHOD
        1. __iter__ should iterate over all slots (including private slots).
        2. __iter_slots__ can return an iterator over:
            a. only public slots or
            b. only private slots or
            c. both
        3. __iter_slots__ will not unpack the slots if they are returned as a tuple, list, dict, or set.
    C. REPRESENTATION DUNDER METHOD
        1. __repr__ should include the repr() of all slots (including private slots).
        2. __repr_private__ can return a string representation of the object with:
            a. only public slots or
            b. only private slots or
            c. both
    D. STRING DUNDER METHOD
        1. __str__ should include only public slots.
        2. __str_private__ can return a string representation of the object with:
            a. only public slots or
            b. only private slots or
            c. both
    E. HASHING
        1. The __hash__ dunder method is not used. (__hash__() expects a type int to be returned)
        2. Hashing a Base Class into a Leaf
            a. Hashes the full representation of the object including private slots.
            b. Can only be used to verify the full representational string of the object.
        3. Hashing a Base Class into a Tree
            a. Hashes each slot into a leaf
            b. Then, hashes the leaves into a tree.
            c. Can be used to verify the findividual slots of the object.
        4. Hashing a Base Class into a Package
            a. Hashes each public slot into a leaf.
            b. Then, hashes the public leaves into a tree.
            c. Next, each private slot is hashed into a leaf.
            d. Then, hashes the private leaves into a tree.
            e. Finally, the public and private trees are hashed together into a tree representing the package.


"""

from abc import ABC
from attrs import define

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

            Example:
                >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
                >>> from attrs import define
                >>> @define(frozen=True, slots=True, weakref_slot=False)
                ... class BaseInterfaceExample(BaseInterface):
                ...     test_property: int = 1
                >>> list(BaseInterfaceExample())
                ['test_property']
        """
        yield from self.__iter_slots__(include_underscored_slots=True, private_only=False)

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
        return f"{self.__class__.__name__}({', '.join([f'{slot}={getattr(self, slot)}' for slot in self.__iter_slots__(include_underscored_slots=include_underscored_slots, private_only=private_only)])})"

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
        for slot in self.__iter_slots__(include_underscored_slots, private_only):
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
    
    def _hash_slots(self, include_underscored_slots: bool = True, private_only: bool = False) -> tuple[str]:
        """Returns the sha256 hash of the representation of each slot in the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample()._hash_slots()
            ('d9e12b2e12010e3b8cd2022e84400d1eb68a4f377069d8759888f6e96082f1e9',)
        """
        hashed_slots: tuple[str] = ()
        for slot in self.__iter_slots__(include_underscored_slots, private_only):
            print(repr(getattr(self, slot)))
            hashed_slots = hashed_slots + (MerkleTree.hash_func(repr(getattr(self, slot))), )

        return hashed_slots

    def _hash_leaf(self, include_underscored_slots: bool = True, private_only: bool = False) -> str:
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
            'd9e12b2e12010e3b8cd2022e84400d1eb68a4f377069d8759888f6e96082f1e9'
        """
        return MerkleTree.hash_func(self.__repr_private__(include_underscored_slots, private_only))

    def _hash_tree(self, include_underscored_slots: bool = True, private_only: bool = False) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            >>> @define(frozen=True, slots=True, weakref_slot=False)
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().hash_tree().root_hash
            'b4c5b6872918d107cff29a9b6a0c81e7c2c450dd46285055beb0deefefa04271'
        """
        return MerkleTree(self._hash_slots(include_underscored_slots, private_only))
    
    def _hash_public(self) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().hash_public()
            'd9e12b2e12010e3b8cd2022e84400d1eb68a4f377069d8759888f6e96082f1e9'
        """
        return self._hash_tree(include_underscored_slots=False, private_only=False).root()
    
    def _hash_private(self) -> str:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().hash_private()
            'b4c5b6872918d107cff29a9b6a0c81e7c2c450dd46285055beb0deefefa04271'
        """
        return self._hash_tree(include_underscored_slots=True, private_only=True).root()
    
    def _hash_package(self) -> MerkleTree:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().hash_package().root_hash
            'b4c5b6872918d107cff29a9b6a0c81e7c2c450dd46285055beb0deefefa04271'
        """
        public_hash: str = self._hash_public()
        private_hash: str = self._hash_private()
        return MerkleTree((public_hash, private_hash))
    
    def _verify_item_in_hash_package(self, item: str) -> bool:
        """Returns the hash of the full representation of the object.

        Returns:
            str: The hash of the representation of the object.

        Example:
            >>> from <GROUPS_PIP_PACKAGE_NAME>.base.interface import BaseInterface
            >>> from attrs import define
            ... class BaseInterfaceExample(BaseInterface):
            ...     test_property: int = 1
            >>> BaseInterfaceExample().verify_item_in_hash_package("test_property")
            True
        """
        leaf_hash: str = MerkleTree.hash_func(repr(getattr(self, item)))
        public_tree = self._hash_public()
        private_tree = self._hash_private()

        return public_tree.verify(leaf_hash) or private_tree.verify(leaf_hash)
        

        
