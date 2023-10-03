from src import App
from typing import TypeAlias
from attrs.exceptions import FrozenInstanceError
from src.base import BaseInterface, BaseValue, BaseContainer, BaseSchema

if __name__ == '__main__':
    app = App()
    app.run()
    app.create_types()
    app.create_types2()


base_interface_instance: BaseInterface = BaseInterface()
print([str(slot) for slot in iter(base_interface_instance)])

base_value_instance: BaseValue = BaseValue(1)
print(str(base_value_instance))
print(repr(base_value_instance))

try:
    base_value_instance.value = 2
except FrozenInstanceError:
    print("FrozenInstanceError as expected")

base_value_instance_from_tuple: BaseValue = BaseValue((1, 2))
print(str(base_value_instance_from_tuple))

base_value_instance_from_list: BaseValue = BaseValue([1, 2])
print(str(base_value_instance_from_list))

base_value_instance_from_set: BaseValue = BaseValue({1, 2})
print(str(base_value_instance_from_set))

base_value_instance_from_frozenset: BaseValue = BaseValue(frozenset({1, 2}))
print(str(base_value_instance_from_frozenset))

base_value_instance_from_dict: BaseValue = BaseValue({1: 2})
print(str(base_value_instance_from_dict))

base_value_instance_from_namedtuple: BaseValue = BaseValue((1, 2))
print(str(base_value_instance_from_namedtuple))

vase_container_instance: BaseContainer = BaseContainer((1, 2))
print(str(vase_container_instance))

vase_container_instance: BaseContainer = BaseContainer([1, 2])
print(str(vase_container_instance))

vase_container_instance: BaseContainer = BaseContainer({1, 2})
print(str(vase_container_instance))

vase_container_instance: BaseContainer = BaseContainer(frozenset({1,2}))
print(str(vase_container_instance))

vase_container_instance: BaseContainer = BaseContainer({1: 2})
print(str(vase_container_instance))
print(str(vase_container_instance._package()))

vase_container_instance: BaseContainer = BaseContainer((1, 2))
print(str(vase_container_instance))
print(str(vase_container_instance._package()))

vase_container_instance: BaseContainer = BaseContainer([1, 2])
print(str(vase_container_instance))
print(str(vase_container_instance._package()))

vase_container_instance: BaseContainer = BaseContainer({1, 2})
print(str(vase_container_instance))
print(str(vase_container_instance._package()))
print(repr(vase_container_instance))

sample_sub_schema = BaseSchema({
    "favorite_game": "string",
    "favorite_color": "string",
    "favorite_numbers": "list[int]",
})

sample_schema1 = BaseSchema({
    "name": "string",
    "age": "int",
    "height": "float",
    "is_human": "bool",
    "favorite_foods": "list[str]",
    "favorite_numbers": "list[int]",
    "favorite_numbers2": "tuple[int]",
    "embedded_schema": sample_sub_schema
})


print(str(sample_schema1._sub_schema()))
print(str(sample_schema1._sub_containers()))
print([item for item in iter(sample_schema1)])

sample_schema2 = BaseSchema({
    "schema": sample_schema1,
    "test": "string"
})
print([item for item in iter(sample_schema2)])
key_types = sample_schema2._get_key_types()
print(key_types)
print (sample_schema2._verify_schema())


sample_schema3 = BaseSchema({
    "schema": sample_schema1,
    "test": "string100"
})
print(sample_schema3._verify_schema())