"""Run all tests."""

import unittest

from tests_merkle_tree import TestMerkleTree
from tests_base_interface import TestBaseInterface
from tests_base_types import TestBaseTypes
from tests_base_value import TestBaseValue
from tests_base_container import TestBaseContainer
from tests_base_schema import TestBaseSchema
from tests_unit_nonce import TestUnitNonce
from tests_unit_credential import TestCredential
from tests_unit_data import TestData
from tests_unit_owner import TestOwner


def main():
    """Run the tests."""
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # Utils tests
    test_suite.addTest(loader.loadTestsFromTestCase(TestMerkleTree))

    # Base tests
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseInterface))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseTypes))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseValue))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseContainer))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseSchema))

    # Group Unit tests
    test_suite.addTest(loader.loadTestsFromTestCase(TestUnitNonce))
    test_suite.addTest(loader.loadTestsFromTestCase(TestCredential))
    test_suite.addTest(loader.loadTestsFromTestCase(TestData))
    test_suite.addTest(loader.loadTestsFromTestCase(TestOwner))

    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.verbosity = 2
    runner.run(test_suite)


if __name__ == '__main__':
    main()
