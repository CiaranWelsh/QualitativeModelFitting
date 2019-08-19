import unittest

from qualitative_model_fitting._suite import Suite, GLOBAL_TEST_SUITE
from qualitative_model_fitting._test_factory import TestFactory

from tests import MODEL1, TEST_INPUT1


class SuiteTests(unittest.TestCase):

    def setUp(self) -> None:
        # create some tests
        self.factory = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        # instance = test_case()

    def test_testcase_autoregisters_into_global_suite(self):
        self.factory.create_test_cases()
        expected = 'InsulinOnly'
        actual = GLOBAL_TEST_SUITE.tests[0].__name__
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
