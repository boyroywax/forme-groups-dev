from attrs import define, field, validators, asdict
import json

from ..base.interface import BaseInterface
from .credential import Credential
from .data import Data
from .owner import Owner
from .nonce import Nonce


@define(frozen=True, slots=True, weakref_slot=False)
class GroupUnit(BaseInterface):
    """The Group Unit class holds the Group Unit data
    """

    nonce: Nonce = field(
        validator=validators.instance_of(Nonce))

    owner: Owner = field(
        validator=validators.instance_of(Owner))

    credential: Credential = field(
        validator=validators.instance_of(Credential))

    data: Data = field(
        validator=validators.instance_of(Data))
    
    def to_dict(self):
        return {
            "nonce": asdict(self.nonce),
            "owner": asdict(self.owner),
            "credential": asdict(self.credential),
            "data": asdict(self.data),
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        return cls(
            nonce=data["nonce"],
            owner=data["owner"],
            credential=data["credential"],
            data=data["data"],
        )

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return cls.from_dict(data)

__all__ = ["GroupUnit", "Credential", "Data", "Owner", "Nonce"]
