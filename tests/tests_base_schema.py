import unittest
import sys

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
