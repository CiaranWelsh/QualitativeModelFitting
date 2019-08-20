import unittest

from tests import MODEL1, TEST_INPUT1
from qualitative_model_fitting._test_factory import TestFactory
from qualitative_model_fitting._suite import GLOBAL_TEST_SUITE, Suite

class TestMakerTests(unittest.TestCase):

    def tearDown(self) -> None:
        GLOBAL_TEST_SUITE.clear()

    def test_dynamic_class_creation(self):
        statement = 'IRS1a@t=10 > Akt@t=10'
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        self.assertEqual('InsulinOnly', GLOBAL_TEST_SUITE[0].__name__)

    def test_alternative_suite(self):
        suite = Suite(name='test_suite')
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101, suite=suite)
        expected = 'InsulinOnly'
        actual = suite[0].__name__
        self.assertEqual(expected, actual)

    def test_registered_by_metaclass(self):
        t = TestFactory(MODEL1, TEST_INPUT1, 0, 100, 101)
        test_cls = GLOBAL_TEST_SUITE[0]
        expected = "<class 'qualitative_model_fitting._case.TestCaseMeta'>"
        actual = str(type(test_cls))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
