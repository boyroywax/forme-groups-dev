import unittest
import sys
import random

sys.path.append("/Users/j/Documents/Forme/code/forme-groups-python-3-12/")


from app.src.base.schema import BaseSchema

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

    def test_get_key_types_from_schema_function(self):
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
        self.assertEqual(person_schema._get_key_types_from_schema(), {'string', 'number', 'schema', 'list[dict[str, str]]'})

    def test_unpack_strings(self):
        packed_string = "schema:person_schema"
        self.assertEqual(BaseSchema._unpack_strings(packed_string), 'schema')

    def test_unpack_strings2(self):
        packed_string = "list[dict[str, str]]"
        self.assertEqual(BaseSchema._unpack_strings(packed_string), 'str, str')

    def test_verify_base_types(self):
        packed_text = ["string", "number", "boolean", "integer", "integer1"]
        self.assertEqual(BaseSchema._verify_base_types(packed_text), (False, "Key type 'integer1' is not valid. "))

    def test_verify_base_types2(self):
        packed_text = ["string", "number", "boolean", "integer"]
        self.assertEqual(BaseSchema._verify_base_types(packed_text), (True, ""))

    def test_verify_base_types3(self):
        packed_text = ["string", "number", "boolean", "integer", "list"]
        self.assertEqual(BaseSchema._verify_base_types(packed_text), (False, "Key type 'list' is not valid. "))

    def test_verify_base_types4(self):
        packed_text = ["string", "number", "boolean", "integer", "list[dict[str, str]]"]
        self.assertEqual(BaseSchema._verify_base_types(packed_text), (False, "Key type 'list[dict[str, str]]' is not valid. "))

    def test_iter(self):
        self.maxDiff = None
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
        items = [item.__str__() for item in iter(person_schema)]
        self.assertEqual(items, ["{'name': 'string'}", "{'age': 'number'}", "{'address': 'schema'}", "{'street': 'string'}", "{'city': 'string'}", "{'state': 'string'}", "{'zip': 'string'}", "{'metadata': 'list[dict[str, str]]'}"])

    def test_str(self):
        self.maxDiff = None
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
        self.assertEqual(person_schema.__str__(), "name: string, age: number, address: schema, street: string, city: string, state: string, zip: string, metadata: list[dict[str, str]]")

    def test_repr(self):
        self.maxDiff = None
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
        self.assertEqual(person_schema.__repr__(), "BaseSchema(schema={name: string, age: number, address: schema, street: string, city: string, state: string, zip: string, metadata: list[dict[str, str]]})")

    def test_has_slots(self):
        self.maxDiff = None
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
        self.assertEqual(person_schema.__slots__, ('_schema',))