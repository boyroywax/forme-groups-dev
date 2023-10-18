import unittest
import sys
from attrs import define

sys.path.append("../forme-groups-python-3-12/")
from src.groups.base.interface import BaseInterface


class TestBaseInterface(unittest.TestCase):
    def setUp(self):

        @define(frozen=True, slots=True, weakref_slot=False)
        class base_interface(BaseInterface):
            test_property: int = 1
            _private_test_property: int = 2

        self.base_interface = base_interface()

        @define(frozen=True, slots=True, weakref_slot=False)
        class BaseInterfaceExample(BaseInterface):
            test_property: int = 1
            test_string: str = "test"
            test_bool: bool = True
            test_float: float = 1.0
            test_bytes: bytes = b"test"
            test_none: None = None
            _private_test_property: int = 2

        self.base_interface2 = BaseInterfaceExample()

    def test_base_interface_init_(self):
        self.assertEqual(self.base_interface.__slots__, ("test_property", "_private_test_property"))

    def test_base_interface_has_slots(self):
        self.assertEqual(len(self.base_interface.__slots__), 2)

    def test_base_interface_has_no_weakref_slot(self):
        self.assertFalse(hasattr(self.base_interface, "__weakref__"))

    def test_base_interface_has_no_dict(self):
        self.assertEqual(hasattr(self.base_interface, "__dict__"), False)

    def test_base_interface_str(self):
        self.assertEqual(str(self.base_interface), "test_property: 1")

    def test_base_interface_repr(self):
        self.assertEqual(repr(self.base_interface), "base_interface(test_property=1, _private_test_property=2)")

    def test_base_interface_hash_repr(self):
        self.assertEqual(self.base_interface._hash_repr(), "d9e12b2e12010e3b8cd2022e84400d1eb68a4f377069d8759888f6e96082f1e9")

    def test_base_interface_iter(self):
        self.assertEqual(list(self.base_interface), ["test_property", "_private_test_property"])
        self.assertEqual(getattr(self.base_interface, "test_property"), 1)
        self.assertEqual(getattr(self.base_interface, "_private_test_property"), 2)

    def test_base_interface_is_frozen(self):
        with self.assertRaises(AttributeError):
            self.base_interface.test_property = 2

    def test_base_interface_more_properties(self):

        self.assertEqual(self.base_interface2._hash_repr(), "d463cd8fc83ebb139815e95d7d49e3a4a97cae611547c0a25c717664f9b59bea")

        self.assertEqual(str(self.base_interface2), "test_property: 1, test_string: test, test_bool: True, test_float: 1.0, test_bytes: b'test', test_none: None")
        self.assertEqual(repr(self.base_interface2), "BaseInterfaceExample(test_property=1, test_string='test', test_bool=True, test_float=1.0, test_bytes=b'test', test_none=None, _private_test_property=2)")

    def test_base_interface2_is_frozen(self):
        with self.assertRaises(AttributeError):
            self.base_interface2.test_property = 2

    def test_base_interface_only_private_str(self):
        self.assertEqual(self.base_interface.__str_private__(include_underscored_slots=True, private_only=True), "_private_test_property: 2")

    def test_base_interface_only_private_repr(self):
        self.assertEqual(self.base_interface.__repr_private__(include_underscored_slots=True, private_only=True), "base_interface(_private_test_property=2)")

    def test_base_interface_only_private_iter(self):
        self.assertEqual(list(self.base_interface.__iter_slots__(include_underscored_slots=True, private_only=True)), ["_private_test_property"])
        self.assertEqual(getattr(self.base_interface, "_private_test_property"), 2)

    def test_base_interface_hash_public(self):
        self.assertEqual(self.base_interface._hash_public_slots(), "3eff7c5314a5ed2d5d8fdad16bbc4851cd98b9861c950854246318c5576a37fd")

    def test_base_interface_hash_private(self):
        self.assertEqual(self.base_interface._hash_private_slots(), "32ee78186a3407f4f288673b1a7dca6154c294f435f444ee3ba054356a88a1e8")

    def test_base_interface_hash_package(self):
        self.maxDiff = None
        self.assertEqual(self.base_interface._hash_package().root(), "d851ff37270107d87981c2adab6bd7eae16d5ee0187b213ffc1564b148a23b9a")

    def text_base_interface_hash_package_verify(self):
        self.maxDiff = None
        self.assertTrue(self.base_interface._hash_package().verify(self.base_interface._hash_repr()))

    def test_base_interface2_hashes(self):
        self.assertEqual(self.base_interface2._hash_repr(), 'd463cd8fc83ebb139815e95d7d49e3a4a97cae611547c0a25c717664f9b59bea')
        self.assertEqual(self.base_interface2._hash_slots(), ('6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
            '6e94a0aef218fd7aef18b257f0ba9fc33c92a2bc9788fc751868e43ab398137f',
            '3cbc87c7681f34db4617feaa2c8801931bc5e42d8d0f560e756dd4cd92885f18',
            'd0ff5974b6aa52cf562bea5921840c032a860a91a3512f7fe8f768f6bbe005f6',
            '82fb6f322c62a7f4c9869b7a91e2f16ecd8113aa9fd797216d473bd00764b43d',
            'dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91',
            'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35'))
        
        self.assertEqual(self.base_interface2._hash_public_slots(), '933c32b6ec12b7f41e028185cc2f347d3051c2561d70d48f62fb38f47c18a772')
        self.assertEqual(self.base_interface2._hash_private_slots(), '32ee78186a3407f4f288673b1a7dca6154c294f435f444ee3ba054356a88a1e8')
        self.assertEqual(self.base_interface2._hash_package().root(), 'a4ad9b7196e928dd5b02374a2ddea89260fafe65cc84378451c06fd96b02c4fc')

