
"""Run all tests."""

import unittest

# from .tests_general import TestsGeneral
from tests_base_container import TestBaseContainer


def main():
    """Run the tests."""
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    # test_suite.addTest(loader.loadTestsFromTestCase(TestsGeneral))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBaseContainer))

    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.verbosity = 2
    runner.run(test_suite)


if __name__ == '__main__':
    main()
