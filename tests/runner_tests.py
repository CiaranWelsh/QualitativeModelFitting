import unittest

from qualitative_model_fitting._parser import Parser
from qualitative_model_fitting._interpreter import *
from qualitative_model_fitting._runner import ManualRunner
from tests import MODEL1


class TestRunner(unittest.TestCase):

    def setUp(self) -> None:
        string = """
          timeseries InsulinOnly {
              Insulin=1, Rapamycin=0, AA=0
          } 0, 100, 101
          timeseries InsulinAndRapa {
              Insulin=1, Rapamycin=1
          } 0, 100, 101
          timeseries InsulinAndRapaAndAA {
              Insulin=1, Rapamycin=1, AA=0.3
          } 0, 100, 101

          observation 
              Obs1: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=10
              Obs2: mean Akt[InsulinOnly]@t=(0, 100) > all Akt[InsulinAndRapa]@t=10
          """
        parser = Parser()
        self.tree = parser.parse(string)
        self.interpreter = Interpreter(self.tree)

    def test_time_series_is_run(self):
        ts, obs = self.interpreter.interpret()
        runner = ManualRunner(MODEL1, ts, obs)
        dct = runner._run_timeseries()
        expected = sorted(['InsulinOnly', 'InsulinAndRapa', 'InsulinAndRapaAndAA'])
        actual = sorted(list(dct.keys()))
        self.assertEqual(expected, actual)

    def test_run(self):
        ts, obs = self.interpreter.interpret()
        runner = ManualRunner(MODEL1, ts, obs)
        expected = {'Obs1: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=10': {'truth': True}, 'Obs2: mean Akt[InsulinOnly]@t=(0, 100) > all Akt[InsulinAndRapa]@t=10': {'truth': True}}
        actual = runner.run()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
