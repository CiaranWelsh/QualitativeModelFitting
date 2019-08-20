import pandas as pd
from typing import Optional

from qualitative_model_fitting import TestCase
from qualitative_model_fitting import TimeSeries
from qualitative_model_fitting._suite import GLOBAL_TEST_SUITE, Suite


class TestFactory:
    """
    Factory class that builds TestCases on the fly.
    """

    def __init__(self, ant_str: str, inputs: dict,
                 time_start: (int, float), time_end: (int, float),
                 steps: int, suite: Optional[Suite]):
        self.ant_str = ant_str
        self.inputs = inputs
        self.time_start = time_start
        self.time_end = time_end
        self.steps = steps
        self.suite = suite

        self.time_series_data = self._run_timeseries()

        self.suite = self.create_test_suite()

    def _run_timeseries(self) -> pd.DataFrame:
        """
        wrapper around TimeSeries. Simulate time series data
        for testing conditions.

        Returns:

        """
        return TimeSeries(
            self.ant_str, self.inputs,
            self.time_start, self.time_end, self.steps
        ).simulate()

    def create_test_suite(self) -> Suite:
        """
        Iterate over conditions and create subclasses of
        type TestCase. If suite not specified in constructor
        objects are automatically stored in the GLOBAL_TEST_SUITE

        Returns:

        """
        for condition_name, condition_dict in self.inputs.items():
            data = self.time_series_data[condition_name]
            obs = condition_dict['obs']
            # automatically added to GLOBAL_TEST_SUITE by TestCaseMeta
            cls = type(condition_name, (TestCase,), {'data': data, 'obs': obs})
            if self.suite is not None:
                #  might be better to put the running code in Runner.
                if self.suite.name == 'global_test_suite':
                    raise ValueError('Do not set the "suite" argument to '
                                     'the GLOBAL_TEST_SUITE because all tests '
                                     'are automatically accumulated into '
                                     'GLOBAL_TEST_SUITE anyway. Instead, import'
                                     ' the GLOBAL_TEST_SUITE from _suite module.')
                self.suite.append(cls)
        if self.suite:
            return self.suite
        else:
            return GLOBAL_TEST_SUITE

