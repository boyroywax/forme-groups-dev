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
        self.load_state()

    def load_state(self):
        with open(self.state_file, 'r') as f:
            state = json.load(f)
            active_state = state.get('active')
            # print(f'Loading state: {json.loads(state)}')
            print(f'action_state: {active_state=}')
            if active_state:
                self.controller._add_group_unit(GroupUnit.from_dict(active_state))

    def save_state(self):
        state = {
            'active': self.controller.active.to_json() if self.controller.active else []
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=4, default=GroupUnit.from_json)

    def json_encoder(self, obj):
        if isinstance(obj, GroupUnit):
            return obj.to_dict()
        return obj

    # def load_state(self):
    #     if os.path.exists(self.state_file):
    #         try:
    #             with open(self.state_file, 'r') as f:
    #                 state: str = json.read(f)
    #                 print(type(state))


    #             self.controller.active = GroupUnit.from_dict(state['active'])
    #                 # self.save_state()
    #         except Exception as e:
    #             print(e)
    #             print("Error loading state, creating new state file")
    #             self.save_state()
    #     # else:
    #     #     self.save_state()

    # def save_state(self):
    #     state = {
    #         'active': self.controller.active.to_json()
    #     }
    #     print(f'Saving state: {state=}')
    #     with open(self.state_file, 'w') as f:
    #         json.dump(state, f, indent=4)

    def __del__(self):
        self.save_state()

    

__all__ = [
    "Groups"
]
