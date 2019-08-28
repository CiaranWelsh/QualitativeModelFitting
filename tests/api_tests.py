import unittest

from collections import OrderedDict
from qualitative_model_fitting._api import manual_interface
from qualitative_model_fitting._simulator import TimeSeriesPlotter, TimeSeries

from tests import MODEL2


class ManualInterfaceTests(unittest.TestCase):

    def setUp(self) -> None:
        self.input = """
          timeseries None {
              S=0, I=0
          } 0, 100, 101
          timeseries S {
              S=1, I=0
          } 0, 100, 101
          timeseries I {
              S=0, I=1
          } 0, 100, 101
          timeseries SI {
              S=1, I=1
          } 0, 100, 101

          observation 
              Obs1: A[None]@t=0 > A[S]@t=10
              Obs2: mean B[SI]@t=(0, 100) > C[I]@t=10
              Obs3: C[SI]@t=10 == A[None]@t=10
          """

    def test_correct_number_of_observations(self):
        results = manual_interface(MODEL2, self.input)
        expected = 3
        actual = results.shape[0]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
