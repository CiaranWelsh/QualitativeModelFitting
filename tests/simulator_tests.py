import unittest
import os, glob
import yaml

from collections import OrderedDict

from .model_strings import *
from qualitative_model_fitting._simulator import *


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
            pass
            # os.remove(self.yaml_file)

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


if __name__ == '__main__':
    unittest.main()
