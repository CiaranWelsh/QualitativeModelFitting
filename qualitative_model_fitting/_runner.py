import os, glob
import numpy as np
import pandas as pd

from qualitative_model_fitting._suite import Suite
from qualitative_model_fitting._simulator import TimeSeries
from typing import Optional


class _RunnerBase:

    def __init__(self, suite: Optional[Suite], timeseries_kwargs={}):
        self.suite = suite
        self.timeseries_kwargs = timeseries_kwargs

    def _run_timeseries(self) -> dict:
        for i in ['ant_str', 'inputs', 'time_start',
                  'time_end', 'steps']:
            if not self.timeseries_kwargs.get(i):
                raise AttributeError(f'Please give argument "{i}" to '
                                     f'timeseries_kwargs dict')

        return TimeSeries(**self.timeseries_kwargs).simulate()


class ManualRunner(_RunnerBase):

    def run_tests(self):
        print('run tests')
        for test_case in self.suite:
            test = test_case()
            # todo ensure make_tests dict return a set of bound functions so we do not have to
            #  pass test_case back into the function as argument.
            # todo ensure tests are producted for all statements.
            print(test.make_tests()['test_statement_0'](test_case))
            # test = test_case().make_tests()
            # for k, v in test.items():
            #     print(k, v)
            #     v(test)


class AutomaticRunner(_RunnerBase):
    pass
