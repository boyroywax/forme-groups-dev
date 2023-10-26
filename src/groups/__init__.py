from attrs import define, field, Factory, validators, asdict
import os
import json
from io import open


from .controller import Controller
from .unit import GroupUnit


@define(slots=True, weakref_slot=False)
class Groups:
    controller: Controller = field(
        validator=validators.instance_of(Controller),
        default=Factory(Controller))
    
    state_file: str = field(
        validator=validators.instance_of(str),
        default='groups.json')

    def __init__(self, state_file='groups.json'):
        self.controller = Controller()
        self.state_file = state_file
        # self.load_state()

    def load_state(self):
        with open(self.state_file, 'r') as f:
            state = json.load(f)
            active_state = state.get('active')
            if active_state:
                self.controller._add_group_unit(GroupUnit.from_dict(active_state))

    def save_state(self):
        state = {
            'active': self.controller.active
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=4, default=self.json_encoder)

    def json_encoder(self, obj):
        if isinstance(obj, GroupUnit):
            return obj.to_dict()
        return obj

    def __del__(self):
        self.save_state()

    

__all__ = [
    "Groups"
]
