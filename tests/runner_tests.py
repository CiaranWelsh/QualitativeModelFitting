import unittest

from qualitative_model_fitting._runner import _RunnerBase, ManualRunner, AutomaticRunner
from qualitative_model_fitting._test_factory import TestFactory
from qualitative_model_fitting._suite import GLOBAL_TEST_SUITE

from tests import TEST_INPUT1, MODEL1, TEST_INPUT2


class RunnerTests(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = TestFactory(MODEL1, TEST_INPUT2, 0, 100, 101)

    def test_something(self):
        print(self.factory)
        print(GLOBAL_TEST_SUITE)
        print(GLOBAL_TEST_SUITE.tests)
        # runner = ManualRunner(GLOBAL_TEST_SUITE)
        # runner.run_tests()


if __name__ == '__main__':
    unittest.main()
