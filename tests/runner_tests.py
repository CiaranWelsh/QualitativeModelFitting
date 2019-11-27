import unittest
import logging

from qualitative_model_fitting._parser import Parser
from qualitative_model_fitting._runner import Runner
from tests import MODEL1, MODEL2


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
        runner = Runner(MODEL1, string)
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

    def test_run_qmf(self):
        import qualitative_model_fitting as qmf

        input_string = '''
        timeseries None { S=0, I=0 } 0, 100, 101
        timeseries S { S=1, I=0 } 0, 100, 101
        timeseries I { S=0, I=1 } 0, 100, 101
        timeseries SI { S=1, I=1 } 0, 100, 101
        observation
            Obs_basics1:    A[None]@t=0             >  A[None]@t=10
            Obs_basics2:    A[S]@t=10               >  A[S]@t=0
            Obs_basics3:    A[S]@t=25               >  A[SI]@t=25
            Obs_mean:       mean(B[S]@t=(0, 100))   >  mean(B[SI]@t=(0, 100))
            Obs_max:        max(B[SI]@t=(0, 100))   >  max(B[S]@t=(0, 100))
            Obs_min:        min(B[SI]@t=(0, 100))   == 0
            Obs_any:        any(B[SI]@t=(0, 100)    >  3)
            Obs_all:        all(B[S]@t=(0, 100)     <  1) 
        '''
        runner = qmf.Runner(MODEL2, input_string)
        print(runner.run())



if __name__ == '__main__':
    unittest.main()
