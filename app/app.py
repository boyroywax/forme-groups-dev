from src import App
from src.base import BaseInterface
from typing import TypeAlias
from attrs.exceptions import FrozenInstanceError

if __name__ == '__main__':
    app = App()
    app.run()
    app.create_types()
    app.create_types2()

    value: BaseInterface = BaseInterface(1)
    number: TypeAlias = int | float
    print(value)
    print(value._value)
    print(isinstance(value, BaseInterface))
    print(isinstance(value._value, number))
    print(type(value._value))
    print(value._slots_to_string())

    value2: BaseInterface = BaseInterface([1.0, 2.0, 3.0, "string1"])
    print(value2)
    print(repr(value2))
    print(value2._is_type())
    print([item for item in iter(value2)])

    value3: BaseInterface = BaseInterface({"key1": "value1", "key2": "value2"})
    print(value3)
    print(repr(value3))
    print(value3._is_type())
    print([item for item in iter(value3)])

    value4: BaseInterface = BaseInterface({"key1": "value1", "key2": "value2", "key3": {"key4": "value4", "key5": "value5", "key6": {"key7": "value7", "key8": "value8", "key9": "value9"}}})
    print(value4)
    print(repr(value4))
    print(value4._is_type())
    print(value4._get_max_sublevel())
    print([item for item in iter(value4)])

    value5: BaseInterface = BaseInterface({"key1": ["value1", "value2", {"key2": "value3"}, {"key3": (1,2,3,[1, [0, [0, [0]]]])}], "key02": {"key021": "value021", "key170": ["value170"]}})
    print(value5)
    print(repr(value5))
    print(value5._is_type())
    print(value5._get_max_sublevel())
    print([item for item in value5.iter_to_depth(8)])

    try:
        value5._value = {"key1": "value1"}
    except FrozenInstanceError as e:
        print(str(e))

    print(value5)
