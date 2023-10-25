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
            "nonce": self.nonce._to_dict(),
            "owner": self.owner._to_dict(),
            "credential": self.credential._to_dict(),
            "data": self.data._to_dict(),
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        return cls(
            nonce=Nonce._from_dict(data.get("nonce")),
            owner=Owner._from_dict(data["owner"]),
            credential=Credential._from_dict(data["credential"]),
            data=Data._from_dict(data["data"]),
        )

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return cls.from_dict(data)
    
    def _print(self):
        return (f"Group Unit:\n"
            f"Nonce: {self.nonce._get_active().value}\n"
            f"Owner: {self.owner.owner.__str__()}\n"
            f"Credential: {self.credential.credential.__str__()}\n"
            f"Data: {self.data.entry._to_dict()}")

__all__ = ["GroupUnit", "Credential", "Data", "Owner", "Nonce"]
