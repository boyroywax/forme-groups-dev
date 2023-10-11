
"""Run all tests."""

import unittest

from tests_base_interface import TestBaseInterface
from tests_base_types import TestBaseTypesInterface
from tests_base_types import TestBaseValueTypes, TestBaseContainerTypes
from tests_base_value import TestBaseValue
# from tests_base_container import TestBaseContainer
# from tests_base_schema import TestBaseSchema


def main():
    """Run the tests."""
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseInterface))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseTypesInterface))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseValueTypes))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseContainerTypes))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseValue))
    # test_suite.addTest(loader.loadTestsFromTestCase(TestBaseContainer))
    # test_suite.addTest(loader.loadTestsFromTestCase(TestBaseSchema))

    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.verbosity = 2
    runner.run(test_suite)


if __name__ == '__main__':
    main()
