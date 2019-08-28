import unittest

from qualitative_model_fitting._parser import Parser

tests = [
    "word > other",
    "IRS1a[condition]@t=10 > Akt[condition]@t=10"
]


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()

    def test_something(self):
        string = """
        timeseries InsulinOnly {
            Insulin=1, Rapamycin=0, AA=0
        } 0, 100, 101
        timeseries InsulinAndRapa {
            Insulin=1, Rapamycin=1
        } 0, 100, 101
        timeseries InsulinAndRapaAndAA {
            Insulin=1, Rapamycin=1, AA=1.0
        } 0, 100, 101
        
        observation 
            Obs1: Akt[Insulin]@t=0 > Akt[InsulinAndRapa]@t=10
            Obs2: mean Akt[Insulin]@t=(0,100) > Akt[InsulinAndRapa]@t=10
            Obs3: all Akt[InsulinAndRapa]@t=(0, 100) == 0
        """

        expected = """start
  block
    _timeseries_block
      Insulin
      ts_arg
        Insulin
        1
        ts_arg
          Rapamycin
          0
      0
      100
      101
  block
    _timeseries_block
      InsulinAndRapa
      ts_arg
        Insulin
        1
        ts_arg
          Rapamycin
          1
      0
      100
      101
  block
    observation_block
      statement
        clause
          Akt
          Insulin
          0
        gl
        clause
          Akt
          InsulinAndRapa
          10
      statement
        clause
          mean
          Akt
          Insulin
          0
        gl
        clause
          Akt
          InsulinAndRapa
          10"""
        actual = self.parser.pretty(string)
        print(actual)
        # self.assertEqual(expected.strip(), actual.strip())


if __name__ == '__main__':
    unittest.main()
