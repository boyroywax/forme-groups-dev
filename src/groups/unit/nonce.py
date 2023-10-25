from attrs import define, field
from typing import override, Optional

from ..base.interface import BaseInterface
from ..base.types import BaseTypes
from ..base.value import BaseValue
from ..base.container import BaseContainer
from ..base.exceptions import GroupBaseException
from ..utils.crypto import MerkleTree

__DEFAULT_NONCE_SEPERATOR__ = '.'
__SUPPORTED_NONCE_TYPES__ = (str, int)


def _validate_nonce_type(instance, attribute, value):
    """Validates the argument is a supported nonce type

    Args:
        instance (Any): The instance
        attribute (Any): The attribute
        value (Any): The value

    Raises:
        GroupNonceException: If the value is not a supported nonce type
    """
    if not isinstance(value, BaseContainer):
        raise GroupBaseException(f"Expected a BaseContainer, but received {type(value)}")

    for item_ in value.items:
        if not isinstance(item_, BaseValue):
            raise GroupBaseException(f"Expected a BaseValue, but received {type(item_)}")

        if not isinstance(item_.value, int | str):
            raise GroupBaseException(f"Expected a supported nonce type, but received {type(item_.value)}")


@define(frozen=True, slots=True, weakref_slot=False)
class Nonce(BaseInterface):
    """
    The Nonce class holds the nonce chain of the Group Unit
    """

    _chain: BaseContainer = field(
        validator=_validate_nonce_type,
        default=BaseContainer((BaseValue(0),)))

    def _get_active(self) -> BaseValue:
        """Sets the active nonce

        """
        return self._chain.items[-1]

    def _next_active(self) -> BaseValue:
        """Gets The next active nonce
        """
        active_nonce = self._get_active()
        if isinstance(active_nonce.value, int):
            return BaseValue(active_nonce.value + 1)

        elif isinstance(active_nonce.value, str):
            if active_nonce.value[-1] == 'z':
                return BaseValue(active_nonce.value + 'a')
            elif active_nonce.value[-1] == 'Z':
                return BaseValue(active_nonce.value + 'A')

            next_char = chr(ord(active_nonce.value[-1]) + 1)
            return BaseValue(active_nonce.value[:-1] + next_char)

    def _next_active_chain(self) -> BaseContainer:
        """Gets the next active chain
        """
        return BaseContainer(self._chain.items[:-1] + (self._next_active(),))

    def _next_active_nonce(self) -> 'Nonce':
        """Gets the next active nonce
        """
        return Nonce(self._next_active_chain())
    
    def _next_sub_nonce_chain(self, type_: type) -> BaseContainer:
        """Determines the next sub nonce chain
        """
        match str(type_):
            case "<class 'int'>":
                return BaseContainer(self._chain.items + (BaseValue(0),))
            case "<class 'str'>":
                return BaseContainer(self._chain.items + (BaseValue('a'),))
            case _:
                raise NotImplementedError(f"Unsupported type {type_}")
    
    def _next_sub_nonce(self, type_alias: Optional[str] = None) -> 'Nonce':
        """Determines the next sub nonce
        """
        if type_alias is None:
            type_alias: str = self._get_active().get_type_str()
        
        type_ = BaseTypes._get_type_from_alias(type_alias)
            
        return Nonce(self._next_sub_nonce_chain(type_))

    @property
    def nonce(self) -> BaseContainer:
        """The nonce of the Group Unit

        Returns:
            str: The nonce of the Group Unit

        Examples:
            >>> nonce = Nonce('nonce')
        """
        return self._chain

    @override
    def __str__(self) -> str:
        """ The items of the nonce chain, seperator by __DEFAULT_NONCE_SEPERATOR__
        """
        return __DEFAULT_NONCE_SEPERATOR__.join(str(item) for item in self._chain.items)

    @override
    def __repr__(self) -> str:
        """ The representation of the nonce chain
        """
        return f'Nonce(chain={repr(self.nonce)})'
    
    @override
    def __iter__(self):
        """ Iterate through the nonce chain
        """
        return iter(self._chain.items)
    
    def _hash_nonce_str(self) -> str:
        return MerkleTree._hash_func(str(str(self)))
    
    def _hash_nonce_units(self) -> tuple[str, ...]:
        nonce_units: tuple = ()
        for nonce_unit in self:
            nonce_units = nonce_units + (nonce_unit._hash().root(), )
        return nonce_units
    
    def _hash(self) -> MerkleTree:
        # return MerkleTree(self._hash_nonce_units())
        return MerkleTree((self._hash_nonce_str(),))
    
    def _to_dict(self) -> dict:
        return {
            "chain": self.nonce._to_dict()
        }
    
    @classmethod
    def _from_dict(cls, _dict: dict) -> 'Nonce':
        # parse the nonce chain
        nonce_chain = BaseContainer._from_dict(_dict['chain'])
        
        return cls(nonce_chain)