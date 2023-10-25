from attrs import define, field, validators, Factory
from typing import Optional, Any

# from src.groups.base.value import BaseValue

from .base import BaseContainer, BaseSchema
from .unit import GroupUnit, Credential, Data, Owner, Nonce
from .pool import Pool

__DEFAULT_GROUP_UNIT__ = GroupUnit(
    Nonce(BaseContainer((0, ), "tuple")),
    Owner(),
    Credential(),
    Data(BaseContainer((0, ), "tuple")))


@define(slots=True, weakref_slot=False)
class Controller:
    """The Controller class holds a Pool of Group Units and is used to manage the Group Units

    Args:
        pool (Optional[Pool]): The Pool of Group Units
    """
    pool: Optional[Pool] = field(
        default=None,
        validator=validators.optional(validators.instance_of(Pool)))
    
    _active: Optional[GroupUnit] = field(
        default=None,
        validator=validators.optional(validators.instance_of(GroupUnit)))

    def __init__(self, pool: Optional[Pool] = None):
        if pool is not None:
            self.pool = pool
        else:
            self.pool = Pool(((__DEFAULT_GROUP_UNIT__.data._hash().root(), __DEFAULT_GROUP_UNIT__.nonce._hash().root(), __DEFAULT_GROUP_UNIT__),), )

        self._active = self.pool.group_units[-1][2]

    @property
    def active(self) -> GroupUnit | None:
        self._active = self.pool.group_units[-1][2]
        return self._active
    
    @active.setter
    def active(self, group_unit: GroupUnit) -> None:
        self._active = group_unit

    def _add_group_unit(self, group_unit: GroupUnit) -> None:
        """Adds a GroupUnit to the Pool

        Args:
            group_unit (GroupUnit): The GroupUnit to add to the Pool
        """
        self.pool.add_group_unit(group_unit)

    def _get_active_nonce(self) -> Nonce:
        """Gets the active nonce

        Returns:
            Nonce: The active nonce
        """
        return self.active.nonce

    def _create_group_unit(
        self,
        data: Data,
        is_sub_unit: Optional[bool] = None,
        super_unit_schema: Optional[BaseSchema] = None,
        super_unit_hash: Optional[str] = None,
        override_nonce: Optional[Nonce] = None
    ) -> GroupUnit:
        """Creates a GroupUnit

        Args:
            data (Data): The Data of the GroupUnit
            is_sub_unit (Optional[bool]): Whether the GroupUnit is a sub Unit. Defaults to None.
            super_unit_schema (Optional[BaseSchema]): The Schema of the super Unit. Defaults to None.
            super_unit_hash (Optional[str]): The hash of the super Unit. Defaults to None.
            override_sub_unit (bool): Whether to override the sub Unit. Defaults to False.
        """
        schema_to_enforce: Optional[BaseSchema] = None
        next_nonce: Optional[Nonce] = None

        if is_sub_unit is None or is_sub_unit is False:
            next_nonce = self.active.nonce._next_active_nonce()

        elif is_sub_unit is True and override_nonce is None:
            if self.active.data.schema is None:
                raise AttributeError("Cannot create a sub Unit without a schema")
            next_nonce = self.active.nonce._next_sub_nonce()

        elif override_nonce is not None:
            next_nonce = override_nonce

        if super_unit_schema is not None and super_unit_hash is not None:
            raise ValueError("Cannot set both super_unit_schema and super_unit_hash")
        elif super_unit_schema is None and super_unit_hash is None:
            schema_to_enforce = self.active.data.schema
        elif super_unit_schema is None and super_unit_hash is not None:
            super_unit = self._get_group_unit(super_unit_hash)
            schema_to_enforce = super_unit.data.schema
        elif super_unit_schema is not None and super_unit_hash is None:
            schema_to_enforce = super_unit_schema

        new_data = Data._from(data.entry, data.schema, schema_to_enforce)

        credential = Credential()
        owner = Owner()
        group_unit = GroupUnit(next_nonce, owner, credential, new_data)
        self._add_group_unit(group_unit)
        return group_unit

    def _get_group_unit(self, hash_: str) -> GroupUnit:
        """Gets a GroupUnit from the Pool

        Args:
            hash_ (str): The hash_ of the GroupUnit to get from the Pool

        Returns:
            GroupUnit: The GroupUnit from the Pool
        """
        return self.pool.get_group_unit(hash_)
    
    def _get_group_unit_from_nonce(self, nonce: Nonce) -> GroupUnit:
        """Gets a GroupUnit from the Pool

        Args:
            nonce (Nonce): The nonce of the GroupUnit to get from the Pool

        Returns:
            GroupUnit: The GroupUnit from the Pool
        """
        return self._get_group_unit(nonce._hash().root())
    
    def _group_unit_from_dict(self, data: dict[str, Any]) -> GroupUnit:
        """Creates a GroupUnit from a dict

        Args:
            data (dict[str, Any]): The dict to create the GroupUnit from

        Returns:
            GroupUnit: The GroupUnit created from the dict
        """
        return self._add_group_unit(GroupUnit.from_dict(data))


