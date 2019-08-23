import logging
from qualitative_model_fitting import _case, _simulator, _suite, GLOBAL_TEST_SUITE
import pandas as pd
LOG = logging.getLogger(__name__)


class TestFactory:
    """
    Factory class that builds TestCases on the fly.
    """

    def __init__(self, ant_str: str, inputs: dict,
                 time_start: (int, float), time_end: (int, float),
                 steps: int, suite=None):
        self.ant_str = ant_str
        self.inputs = inputs
        self.time_start = time_start
        self.time_end = time_end
        self.steps = steps
        self.suite = suite

        self.time_series_data = self._run_timeseries()

        self.suite = self.create_test_suite()

    def _run_timeseries(self) -> dict:
        """
        wrapper around TimeSeries. Simulate time series data
        for testing conditions.

        Returns:

        """
        return _simulator.TimeSeries(
            self.ant_str, self.inputs,
            self.time_start, self.time_end, self.steps
        ).simulate()

    def create_test_suite(self) -> _suite.Suite:
        """
        Iterate over conditions and create subclasses of
        type TestCase. If suite not specified in constructor
        objects are automatically stored in the GLOBAL_TEST_SUITE

        Returns:

        """
        for condition_name, condition_dict in self.inputs.items():
            data = self.time_series_data[condition_name] 
            # with pd.option_context(
            #         'display.max_rows', None,
            #         'display.max_columns', None):
            #     LOG.debug('\n{}'.format(data['IRS1a']))
            obs = condition_dict['obs']
            # automatically added to GLOBAL_TEST_SUITE by TestCaseMeta
            LOG.debug(f'\n Defined a new type derived from TestCase called: {condition_name}\n')
            cls = type(condition_name, (_case.TestCase,), {'data': data, 'obs': obs})
            # LOG.debug(f'\n Data associated with {condition_name} is:\n {data}\n')
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
