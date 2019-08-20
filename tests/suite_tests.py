import unittest

from qualitative_model_fitting._suite import Suite
from qualitative_model_fitting import GLOBAL_TEST_SUITE
from qualitative_model_fitting._test_factory import TestFactory

from tests import MODEL1, TEST_INPUT1, TEST_INPUT2


class SuiteTests(unittest.TestCase):

    def setUp(self) -> None:
        pass
        # create some tests
        # instance = test_case()

    def test_testcase_autoregisters_into_global_suite(self):
        TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        expected = 'InsulinOnly'
        actual = GLOBAL_TEST_SUITE.tests[0].__name__
        self.assertEqual(expected, actual)

    def test_iterator(self):
        # build factory
        TestFactory(MODEL1, TEST_INPUT2, 0, 100, 101)
        # create tests
        # tests are automatically registered to global test suite
        expected = ['InsulinOnly', 'InsulinAndRapamycin']
        actual = []
        for i in GLOBAL_TEST_SUITE:
            actual.append(i.__name__)
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
