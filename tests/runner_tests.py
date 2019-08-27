import unittest

from qualitative_model_fitting import _runner, GLOBAL_TEST_SUITE
from qualitative_model_fitting._test_factory import TestFactory
from qualitative_model_fitting import _suite

from tests import TEST_INPUT1, MODEL1, TEST_INPUT2


class RunnerTests(unittest.TestCase):

    def setUp(self) -> None:
        self.factory = TestFactory(MODEL1, TEST_INPUT2, 0, 100, 101)

    def test_manual_runner(self):
        runner = _runner.ManualRunner(GLOBAL_TEST_SUITE)
        result = runner.run_tests()
        expected = False
        actual = result['InsulinAndRapamycin']['IRS1a@t=10 > Akt@t=10']
        self.assertEqual(expected, actual)

    def test_to_df(self):
        runner = _runner.ManualRunner(suite=GLOBAL_TEST_SUITE)
        result = runner.run_tests().to_df()
        expected = False
        actual = result.iloc[0, 1]
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()