from ._test_factory import TestFactory
from qualitative_model_fitting import GLOBAL_TEST_SUITE
from ._runner import ManualRunner


def manual_interface(ant_str, inputs):
    TestFactory(ant_str, inputs)
    runner = ManualRunner(GLOBAL_TEST_SUITE)
    results = runner.run_tests()
    return results.to_df()


def automatic_interface():
    pass
