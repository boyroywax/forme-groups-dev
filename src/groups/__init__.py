from attrs import define, field, Factory, validators

from .controller import Controller


@define(slots=True, weakref_slot=False)
class Groups:
    controller: Controller = field(
        validator=validators.instance_of(Controller),
        default=Factory(Controller))
    

__all__ = [
    "Groups"
]
