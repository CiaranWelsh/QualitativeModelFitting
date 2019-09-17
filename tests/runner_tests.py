import unittest
import logging

from qualitative_model_fitting._parser import Parser
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
    def runner_func(obs):
        string = TIMESERIES_STRING + '\nobservation\n\t' + obs
        runner = ManualRunner(MODEL1, string)
        return runner

    def test_runner1(self):
        obs = 'Obs1: 5 > 4'
        runner = self.runner_func(obs)
        df = runner.run()
        self.assertTrue(df.loc[0, 'evaluation'])

    def test_runner2(self):
        obs = """
        Obs1: 5 > 4
        Obs2: IRS1a[InsulinOnly]@t=20 > IRS1a[InsulinAndRapa]@t=20
        """
        runner = self.runner_func(obs)
        df = runner.run()
        self.assertTrue(df.loc[1, 'evaluation'])

    def test_runner3(self):
        obs = """
        Obs1: 5 > 4
        Obs2: max(IRS1a[InsulinOnly]@t=(0, 100)) < max(IRS1a[InsulinAndRapa]@t=(0, 100))
        """
        runner = self.runner_func(obs)
        df = runner.run()
        print(df)
        self.assertFalse(df.loc[1, 'evaluation'])




if __name__ == '__main__':
    unittest.main()
