from qualitative_model_fitting import TimeSeries
from qualitative_model_fitting import TestCase
from qualitative_model_fitting._case import TestCaseMeta
from qualitative_model_fitting._suite import Suite, GLOBAL_TEST_SUITE

'''
The simulator will run all interval_time series at once then the test maker 
will distribute those dataframes along with conditions to test cases. 
the test cases will be collected into a suit and then executed by 
the runner

First get the text part of each statement
then refine the interval_time pount. 
then apply any functions 
then apply any math
'''


# todo make all test cases use a subclass of type metaclass to automatically register them into a collection
# test maker should have all the unit methods which will combine to make the necessary for each class
# Each statement should get its own class


class TestFactory:

    def __init__(self, ant_str, inputs, time_start, time_end, steps, suite=None):
        self.ant_str = ant_str
        self.inputs = inputs
        self.time_start = time_start
        self.time_end = time_end
        self.steps = steps
        self.suite = suite

        self.time_series_data = self._run_timeseries()

        self.suite = self.create_test_suite()

    def _run_timeseries(self):
        return TimeSeries(
            self.ant_str, self.inputs,
            self.time_start, self.time_end, self.steps
        ).simulate()

    def create_test_suite(self):
        for condition_name, condition_dict in self.inputs.items():
            data = self.time_series_data[condition_name]
            obs = condition_dict['obs']
            # automatically added to GLOBAL_TEST_SUITE by TestCaseMeta
            cls = type(condition_name, (TestCase,), {})
            #todo might need to instantiate the objects here??? Might not.
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

