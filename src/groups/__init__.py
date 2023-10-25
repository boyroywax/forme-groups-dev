from attrs import define, field, Factory, validators, asdict
import os
import json


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
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    print(state)
            except Exception as e:
                print(e)
                # print("Error loading state, creating new state file")
                # self.save_state()

    def save_state(self):
        state = {
            'active': self.controller.active.to_json()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=4)

    def __del__(self):
        self.save_state()

    

__all__ = [
    "Groups"
]
