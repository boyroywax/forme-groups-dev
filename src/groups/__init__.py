from attrs import define, field, Factory, validators

from .controller import Controller
from .pool import Pool

@define(slots=True, weakref_slot=False)
class Groups:
    controller: Controller = field(validator=validators.instance_of(Controller),
                                      default=Factory(Controller))
