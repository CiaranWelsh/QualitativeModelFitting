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
        pass


    @staticmethod
    def get_interpreter(obs):
        string = TIMESERIES_STRING + '\nobservation\n\t' + obs
        parser = Parser()
        tree = parser.parse(string)
        interpreter = Interpreter(tree)
        ts, obs = interpreter.interpret()
        return ts, obs

    def test_time_series_is_run(self):
        obs = 'Obs1: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=10'
        ts, obs = self.get_interpreter(obs)
        print(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        dct = runner._run_timeseries()
        expected = sorted(['InsulinOnly', 'InsulinAndRapa', 'InsulinAndRapaAndAA'])
        actual = sorted(list(dct.keys()))
        self.assertEqual(expected, actual)

    def test_run1(self):
        obs = 'Obs1: 5 > 4'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        print(result)
        actual = result[0]['comparison']
        expected = '5 > 4'
        self.assertEqual(expected, actual)

    def test_run2(self):
        obs = 'Obs2: 5 + 6 > 4'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        print(result)
        actual = result[0]['comparison']
        expected = '11 > 4'
        self.assertEqual(expected, actual)

    def test_run3(self):
        obs = 'Obs3: 5*2 + 6 > 4'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        print(result)
        actual = result[0]['comparison']
        expected = '16 > 4'
        self.assertEqual(expected, actual)

    def test_run4(self):
        obs = 'Obs4: 6 + 5*2 > 9'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        print(result)
        actual = result[0]['comparison']
        expected = '16 > 9'
        self.assertEqual(expected, actual)

    def test_run5(self):
        obs = 'Obs5: 6 + 5*2 + 7 > 9'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        print(result)
        actual = result[0]['comparison']
        expected = '23 > 9'
        self.assertEqual(expected, actual)

    def test_run6(self):
        obs = 'Obs6: 6/2.0 + 5*2 + 7 > 9'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        print(result)
        actual = result[0]['comparison']
        expected = '20.0 > 9'
        self.assertEqual(expected, actual)

    def test_run7(self):
        obs = 'Obs7: Akt[InsulinOnly]@t=0 > 5'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        print(result)
        actual = result[0]['comparison']
        expected = '10.0050015500576 > 5'
        self.assertEqual(expected, actual)

    def test_run8(self):
        obs = 'Obs8: Akt[InsulinOnly]@t=0*2 > 5'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        actual = result[0]['comparison']
        expected = '20.0100031001152 > 5'
        self.assertEqual(expected, actual)

    def test_run9(self):
        obs = 'Obs9: Akt[InsulinOnly]@t=0*2 +1 > 5'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        actual = result[0]['comparison']
        expected = '21.0100031001152 > 5'
        self.assertEqual(expected, actual)

    def test_run10(self):
        obs = 'Obs10: 1 + Akt[InsulinOnly]@t=0*2 > 5'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        actual = result[0]['comparison']
        expected = '21.0100031001152 > 5'
        self.assertEqual(expected, actual)

    def test_run11(self):
        obs = 'Obs11: mean Akt[InsulinOnly]@t=(0, 5) > 5'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        actual = result[0]['comparison']
        expected = '7.632460576669665 > 5'
        self.assertEqual(expected, actual)

    def test_run12(self):
        obs = 'Obs12: Akt[InsulinOnly]@t=(0, 5) > 5'
        ts, obs = self.get_interpreter(obs)
        runner = ManualRunner(MODEL1, ts, obs)
        result = runner.run()
        actual = result[0]['comparison']
        expected = '15.2649211533 > 5'
        self.assertEqual(expected, actual)

    # def test_run2(self):
    #     obs = 'Obs2: mean Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=10'
    #     ts, obs = self.get_interpreter(obs)
    #     runner = ManualRunner(MODEL1, ts, obs)
    #     result = runner.run()
    #     expected = "{'Obs2': {Token(OBS_NAME, 'Obs2'): True}}"
    #     self.assertEqual(expected, str(result))
    #
    # def test_run3(self):
    #     obs = 'Obs3: 4 > 5'
    #     ts, obs = self.get_interpreter(obs)
    #     runner = ManualRunner(MODEL1, ts, obs)
    #     result = runner.run()
    #     expected = "{'Obs3': {Token(OBS_NAME, 'Obs3'): False}}"
    #     self.assertEqual(expected, str(result))
    #
    # def test_run4(self):
    #     obs = 'Obs4: 4*2 > 5'
    #     ts, obs = self.get_interpreter(obs)
    #     runner = ManualRunner(MODEL1, ts, obs)
    #     result = runner.run()
    #     expected = '8 > 5'
    #     actual = result['comparison']
    #     self.assertEqual(expected, actual)
    #
    # def test_run5(self):
    #     obs = 'Obs5: 1 + 4*2 + 3 > 6 / 5.0'
    #     ts, obs = self.get_interpreter(obs)
    #     runner = ManualRunner(MODEL1, ts, obs)
    #     result = runner.run()
    #     expected = '8 > 5'
    #     print(result)
    #
    #     # actual = result['comparison']
    #     # self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
