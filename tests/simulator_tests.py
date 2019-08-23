import unittest

from collections import OrderedDict
import os
import yaml
from tests import MODEL1, TEST_INPUT2, TEST_INPUT1
from qualitative_model_fitting._simulator import TimeSeries, TimeSeriesPlotter
import pandas as pd

class TimeSeriesTests(unittest.TestCase):

    def setUp(self) -> None:
        self.yaml_input = OrderedDict(
            InsulinOnly=OrderedDict(
                inputs=OrderedDict(
                    Insulin=1,
                    AA=0,
                    Rapamycin=0
                ),
                obs=[
                    'IRS1a@t=0 < IRS1a@t=20'
                ]
            )
        )
        self.yaml_file = os.path.join(os.path.abspath(''), 'config.yaml')
        with open(self.yaml_file, 'w') as stream:
            yaml.dump(self.yaml_input, stream, default_flow_style=False, allow_unicode=True)
        assert os.path.isfile(self.yaml_file)

        with open(self.yaml_file, 'r') as stream:
            self.config = yaml.load(stream, Loader=yaml.FullLoader)

    def tearDown(self) -> None:
        if os.path.isfile(self.yaml_file):
            os.remove(self.yaml_file)

    def test_read_inputs_from_yaml(self):
        ts = TimeSeries(MODEL1, self.yaml_file, 0, 10, 11)
        actual = ts.inputs['InsulinOnly']['inputs']['Insulin']
        expected = 1
        self.assertEqual(expected, actual)
        
    def test_read_inputs_from_dict(self):
        ts = TimeSeries(MODEL1, self.yaml_input, 0, 10, 11)
        actual = ts.inputs['InsulinOnly']['inputs']['Insulin']
        expected = 1
        self.assertEqual(expected, actual)

    def test_load_model(self):
        ts = TimeSeries(MODEL1, self.yaml_file, 0, 10, 11)
        self.assertTrue(hasattr(ts, 'model'))

    def test_simulate(self):
        ts = TimeSeries(MODEL1, self.yaml_file, 0, 10, 11)
        res = ts.simulate()
        actual = res['InsulinOnly'].shape
        expected = (11, 52)
        self.assertEqual(expected, actual)




class SimpleObservationTest(unittest.TestCase):
    pass


class TimeSeriesPlotterTests(unittest.TestCase):

    def setUp(self) -> None:
        self.yaml_input = OrderedDict(
            InsulinOnly=OrderedDict(
                inputs=OrderedDict(
                    Insulin=1,
                    AA=0,
                    Rapamycin=0
                ),
                obs=[
                    'IRS1a@t=0 < IRS1a@t=20'
                ]
            ),
            InsulinAndAA=OrderedDict(
                inputs=OrderedDict(
                    Insulin=1,
                    AA=1,
                    Rapamycin=0
                ),
                obs=[
                    'IRS1a@t=0 < IRS1a@t=20'
                ]
            )
        )
        self.ts = TimeSeries(MODEL1, self.yaml_input, 0, 10, 11)

    def test_plot_1(self):
        plot_selection = dict(
            IRS1=['IRS1', 'IRS1', 'pIRS1']
        )
        conditions = ['InsulinOnly']
        plotter = TimeSeriesPlotter(
            self.ts.simulate(),
            plot_selection,
            conditions,
            savefig=True,
            fname='test_plot.png'
        )
        print(plotter.data)

    def test_plot_2(self):
        print(self.ts.simulate()['InsulinAndAA'].columns)
        plot_selection = dict(
            Akt=['Akt', 'pAkt'],
            IRS1=['IRS1', 'IRS1a']
        )
        conditions = ['InsulinOnly']
        plotter = TimeSeriesPlotter(
            self.ts.simulate(),
            plot_selection,
            conditions,
            savefig=False,
            fname='test_plot.png'
        )
        print(plotter.plot())


if __name__ == '__main__':
    unittest.main()
