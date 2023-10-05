import unittest
import sys
import random

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.schema import BaseSchema
from app.src.base.container import BaseContainer
from app.src.base.value import BaseValue

class TestBaseSchema(unittest.TestCase):
    def test_init_with_dict(self):
        address_schema = BaseSchema({
            "street": "string",
            "city": "string",
            "state": "string",
            "zip": "string"
        
        })
        person_schema = BaseSchema({
            "name": "string",
            "age": "number",
            "address": address_schema
        })
        self.assertEqual(person_schema._verify_schema(), (True, ""))

    def test_init_with_dict2(self):
        address_schema = BaseSchema({
            "street": "string",
            "city": "string",
            "state": "string",
            "zip": "string"
        
        })
        person_schema = BaseSchema({
            "name": "string",
            "age": "number",
            "address": address_schema,
            "notes": "list[str]",
            "metadata": "list[dict[str, str]]"
        })
        self.assertEqual(person_schema._verify_schema(), (True, ""))

    def test_init_with_large_schema(self):
        type_pool = ["string", "number", "boolean", "integer"]
        container_pool = ["list[", "tuple[", "dict["]
        # random_type = random.choice(type_pool)
        # random_container = random.choice(container_pool)

        for _ in range(100):
            random_type = random.choice(type_pool)
            random_container = random.choice(container_pool)
            random_depth = random.randint(0, 10)
            random_container_: str = random.choice(container_pool) if container_pool != "" else random.choice(container_pool)

            def _random_container(random_container__, random_type) -> str:
                closing_bracket = "]"
                for _ in range(random_depth):
                    random_container__ += random.choice(container_pool)
                    closing_bracket += "]"
                return random_container__ + random_type + closing_bracket
            random_container_string = _random_container(random_container, random_type)
            # random_schema = random.choice([random_container_string + random_type + "]"] if random_container != "" else [random_type])
            random_key = random.choice(["test", "test2", "test3", "test4", "test5"])
            random_schema = {random_key: random_container_string}
            print(random_schema)
            random_schema = BaseSchema(random_schema)
            # print(random_schema)
            self.assertEqual(random_schema._verify_schema(), (True, ""))

    def test_sub_schema_function(self):
        address_schema = BaseSchema({
            "street": "string",
            "city": "string",
            "state": "string",
            "zip": "string"
        
        })
        person_schema = BaseSchema({
            "name": "string",
            "age": "number",
            "address": address_schema
        })
        self.assertEqual(person_schema._sub_schema(), [{'address': address_schema}])

    def test_sub_containers_function(self):
        address_schema = BaseSchema({
            "street": "string",
            "city": "string",
            "state": "string",
            "zip": "string",
            "metadata": "list[dict[str, str]]"
        
        })
        person_schema = BaseSchema({
            "name": "string",
            "age": "number",
            "address": address_schema
        })
        self.assertEqual(person_schema._sub_containers(), [{"metadata": "list[dict[str, str]]"}])

    def test_unpack_schema_function(self):
        address_schema = BaseSchema({
            "street": "string",
            "city": "string",
            "state": "string",
            "zip": "string",
            "metadata": "list[dict[str, str]]"
        
        })
        person_schema = BaseSchema({
            "name": "string",
            "age": "number",
            "address": address_schema
        })
        print(f'{person_schema._unpack_schema(person_schema)}')
        self.assertEqual(person_schema._unpack_schema(person_schema), {'name': 'string', 'age': 'number', 'address': 'schema', 'street': 'string', 'city': 'string', 'state': 'string', 'zip': 'string', 'metadata': 'list[dict[str, str]]'})
        
