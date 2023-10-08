from abc import ABC
from attrs import define

from ..utils.crypto import MerkleTree


@define(slots=True, weakref_slot=False)
class BaseInterface(ABC):
    """
    Base interface for all classes
    """
    def _get_slots(self):
        for slot in self.__slots__:
            yield slot

    def __iter__(self):
        yield from self._get_slots()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join([f'{slot}={getattr(self, slot)}' for slot in self._get_slots()])})"

    def __str__(self) -> str:
        return f"{', '.join([f'{slot}: {getattr(self, slot)}' for slot in self._get_slots()])}"

    def hash_leaf(self) -> str:
        return MerkleTree.hash_func(repr(self))
