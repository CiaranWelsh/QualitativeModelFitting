import unittest

from collections import OrderedDict
import os
import yaml
from tests import MODEL1, TEST_INPUT2, TEST_INPUT1
from qualitative_model_fitting._simulator import TimeSeries, TimeSeriesPlotter
import pandas as pd


class TimeSeriesTests(unittest.TestCase):

    def setUp(self) -> None:
        self.input = dict(
            Insulin=1,
            Rapamycin=0,
            AA=0
        )
        self.nested_input = dict(
            InsulinOnly=dict(
                Insulin=1,
                Rapamycin=0,
                AA=0
            ),
            InsulinAndAA=dict(
                Insulin=1,
                Rapamycin=0,
                AA=1
            )
        )
        self.directory = os.path.abspath('')
        self.fname = 'simulation.png'
        self.sim_file = os.path.join(self.directory, self.fname)


    def tearDown(self) -> None:
        if os.path.isfile(self.sim_file):
            os.remove(self.sim_file)

    def test_non_nested(self):
        ts = TimeSeries(MODEL1, self.input, 0, 10, 11)
        self.assertIsInstance(ts.simulate(), pd.DataFrame)

    def test_nested(self):
        ts = TimeSeries(MODEL1, self.nested_input, 0, 10, 11)
        dct = ts.simulate()
        self.assertIsInstance(dct['InsulinOnly'], pd.DataFrame)

    def test_plot_ts_no_condition(self):
        ts = TimeSeries(MODEL1, self.input, 0, 10, 11)
        plot_selection = dict(S6K=['S6K', 'pS6K'])
        TimeSeriesPlotter(ts, plot_selection, savefig=True,
                          plot_dir=self.directory,
                          fname=self.fname).plot()
        self.assertTrue(os.path.isfile(self.sim_file))


    def test_plot_ts_with_condition(self):
        ts = TimeSeries(MODEL1, self.input, 0, 10, 11)
        plot_selection = dict(
            S6K=['S6K'],
            pS6K=['pS6K'],
        )
        TimeSeriesPlotter(ts, plot_selection, savefig=True,
                          plot_dir=self.directory,
                          fname=self.fname).plot()
        self.assertTrue(os.path.isfile(self.sim_file))








if __name__ == '__main__':
    unittest.main()
