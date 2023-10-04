from abc import ABC
from attrs import define


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