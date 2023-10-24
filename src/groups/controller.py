from attrs import define, field, validators, Factory
from typing import Optional

from src.groups.base.value import BaseValue

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
            self.pool = Pool(((__DEFAULT_GROUP_UNIT__._hash_package().root(), __DEFAULT_GROUP_UNIT__.nonce._hash().root(), __DEFAULT_GROUP_UNIT__),), )

        self._active = self.pool.group_units[-1][2]

    @property
    def active(self) -> GroupUnit | None:
        self._active = self.pool.group_units[-1][2]
        return self._active

    def _add_group_unit(self, group_unit: GroupUnit) -> None:
        """Adds a GroupUnit to the Pool

        Args:
            group_unit (GroupUnit): The GroupUnit to add to the Pool
        """
        self.pool.add_group_unit(group_unit)

    def _create_group_unit(
        self,
        data: Data,
        is_sub_unit: Optional[bool] = None,
        super_unit_schema: Optional[BaseSchema] = None,
        super_unit_hash: Optional[str] = None,
        override_sub_unit: bool = False
    ) -> GroupUnit:
        """Creates a GroupUnit

        Args:
            data (Data): The Data of the GroupUnit
            is_sub_unit (Optional[bool]): Whether the GroupUnit is a sub Unit. Defaults to None.
            super_unit_schema (Optional[BaseSchema]): The Schema of the super Unit. Defaults to None.
            super_unit_hash (Optional[str]): The hash of the super Unit. Defaults to None.

        Returns:
            GroupUnit: The GroupUnit that was created

        Notes:
            If is_sub_unit is True, the super_unit_schema must be the same as the schema of the super Unit
            If is_sub_unit is False, the super_unit_schema must be the same as the schema of the super Unit
            If is_sub_unit is None, the super_unit_schema must be the same as the schema of the super Unit
        """
        schema_to_enforce: Optional[BaseSchema] = None
        next_nonce: Optional[Nonce] = None

        print(f'is_sub_unit: {is_sub_unit}, super_unit_schema: {super_unit_schema}, super_unit_hash: {super_unit_hash}')

        if is_sub_unit is None or is_sub_unit is False:
            next_nonce = self.active.nonce._next_active_nonce()
        else:
            next_nonce = self.active.nonce._next_sub_nonce()

        print(f'next_nonce: {next_nonce}')
        print(f'active: {self.active}')

        predicted_super_nonce = self.pool._get_super_nonce(self.active.nonce)
        predicted_super_nonce_group_unit = self._get_group_unit_from_nonce(predicted_super_nonce)
        predicted_super_nonce_group_unit_schema = predicted_super_nonce_group_unit.data.schema

        print(f'predicted_super_nonce: {predicted_super_nonce}')
        print(f'predicted_super_nonce_group_unit: {predicted_super_nonce_group_unit}')
        print(f'predicted_super_nonce_group_unit_schema: {predicted_super_nonce_group_unit_schema}')

        if super_unit_schema is None and super_unit_hash is None:
            schema_to_enforce = predicted_super_nonce_group_unit_schema

        if super_unit_schema is not None and super_unit_hash is None:
            if super_unit_schema == predicted_super_nonce_group_unit_schema:
                schema_to_enforce = super_unit_schema
            else:
                raise AttributeError("Invalid Arguments")

        if override_sub_unit:
            if super_unit_schema is not None and super_unit_hash is not None:
                assert super_unit_schema == self._get_group_unit(super_unit_hash).data.schema, "Sub Unit schema must match super Unit schema"

        # elif super_unit_hash is not None and super_unit_schema is None:
        #     if self._get_group_unit(super_unit_hash).data.schema == self.active.data.schema:
        #         schema_to_enforce = self._get_group_unit(super_unit_hash).data.schema

        # elif super_unit_schema is not None and super_unit_hash is not None:
        #     if super_unit_schema == self._get_group_unit(super_unit_hash).data.schema:
        #         schema_to_enforce = super_unit_schema

        # elif super_unit_schema is None and super_unit_hash is None:
        #     schema_to_enforce =

        # print(f'schema_to_enforce: {schema_to_enforce}'')


        # if super_unit_schema is None and super_unit_hash is None:
        #     schema_to_enforce = self.active.data.schema
        # elif super_unit_schema is not None:
        #     schema_to_enforce = super_unit_schema
        # elif super_unit_hash is not None:
        #     schema_to_enforce = self._get_group_unit(super_unit_hash).data.schema
        # else:
        #     raise Exception("Invalid Arguments")
        

        # if is_sub_unit is None or is_sub_unit is False:
        #     nonce = self.active.nonce._next_active_nonce()
        #     print(f'nonce: {nonce}')
        #     print(f'active: {self.active}')
        #     if super_unit_schema is not None:
        #         schema_to_enforce = super_unit_schema
        #     elif super_unit_hash is not None:
        #         schema_to_enforce = self._get_group_unit(super_unit_hash).data.schema
        #     else:
        #         super_nonce = Nonce(BaseContainer((item for item in self.active.nonce._chain.items[:1]), ))
        #         print(f'super_nonce: {super_nonce}')
        #         schema_to_enforce = self._get_group_unit_from_nonce(super_nonce).data.schema
                
        # elif is_sub_unit:
        #     nonce = self.active.nonce._next_sub_nonce()
        #     if self.active.data.has_schema:
        #         schema_to_enforce = self.active.data.schema
        #         if super_unit_schema is not None:
        #             assert super_unit_schema == schema_to_enforce, "Sub Unit schema must match super Unit schema"
        #         elif super_unit_hash is not None:
        #             assert self._get_group_unit(super_unit_hash).data.schema == schema_to_enforce, "Sub Unit schema must match super Unit schema"
                
        print(f'schema_to_enforce: {schema_to_enforce}')
        new_data = Data._from(data.entry, data.schema, schema_to_enforce)
        print(f'data: {new_data}')
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

