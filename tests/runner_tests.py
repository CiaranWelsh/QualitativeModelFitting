import unittest
import logging

from qualitative_model_fitting._parser import Parser
from qualitative_model_fitting._interpreter import *
from qualitative_model_fitting._runner import ManualRunner
from tests import MODEL1


TIMESERIES_STRING = """
          timeseries InsulinOnly {
              Insulin=1, Rapamycin=0, AA=0
          } 0, 100, 101
          timeseries InsulinAndRapa {
              Insulin=1, Rapamycin=1
          } 0, 100, 101
          timeseries InsulinAndRapaAndAA {
              Insulin=1, Rapamycin=1, AA=0.3
          } 0, 100, 101
          """

class TestRunner(unittest.TestCase):

    def setUp(self) -> None:
        string = """
          observation 
              //Obs3: 4 > 5
              Obs4: 4*2 < 5
              //Obs5: Akt[InsulinOnly]@t=0*2 < Akt[InsulinAndRapa]@t=10
        """

    @staticmethod
    def interpreter(obs):
        string = TIMESERIES_STRING + '\nobservation\n\t' + obs
        parser = Parser()
        tree = parser.parse(string)
        interpreter = Interpreter(tree)
        ts, obs = interpreter.interpret()
        return ts, obs

    def test_time_series_is_run(self):
        obs = 'Obs1: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=10'
        ts, obs = self.interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        dct = runner._run_timeseries()
        expected = sorted(['InsulinOnly', 'InsulinAndRapa', 'InsulinAndRapaAndAA'])
        actual = sorted(list(dct.keys()))
        self.assertEqual(expected, actual)

    def test_run1(self):
        obs = 'Obs1: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=0'
        ts, obs = self.interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        expected = "{'Obs1': {Token(OBS_NAME, 'Obs1'): False}}"
        self.assertEqual(expected, str(result))

    def test_run2(self):
        obs = 'Obs2: mean Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=10'
        ts, obs = self.interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        expected = "{'Obs2': {Token(OBS_NAME, 'Obs2'): True}}"
        self.assertEqual(expected, str(result))

    def test_run3(self):
        obs = 'Obs3: 4 > 5'
        ts, obs = self.interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        expected = "{'Obs3': {Token(OBS_NAME, 'Obs3'): False}}"
        self.assertEqual(expected, str(result))

    def test_run4(self):
        obs = 'Obs4: 4*2 > 5'
        ts, obs = self.interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        expected = '8 > 5'
        actual = result['comparison']
        self.assertEqual(expected, actual)

    def test_run5(self):
        obs = 'Obs5: 1 + 4*2 + 3 > 6 / 5.0'
        ts, obs = self.interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        expected = '8 > 5'
        print(result)

        # actual = result['comparison']
        # self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
