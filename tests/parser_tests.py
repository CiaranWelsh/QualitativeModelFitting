import unittest

from lark import Token, Tree
from qualitative_model_fitting._parser import Parser
from qualitative_model_fitting._parser import _TimeSeriesBlock, _TimeSeriesArgument, _TimeSeriesArgumentList

from tests import MODEL1, MODEL2


STRING = """
        timeseries InsulinOnly {
            Insulin=1, Rapamycin=0, AA=0
        } 0, 100, 101
        timeseries InsulinAndRapa {
            Insulin=1, Rapamycin=1
        } 0, 100, 101
        timeseries InsulinAndRapaAndAA {
            Insulin=1, Rapamycin=1, AA=1.0
        } 0, 100, 101
        steadystate ss1 {Insulin=1}
"""


class ParserTests(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def get_parsed_observatoin(self, obs):
        string = STRING + 'observation\n\t' + obs
        return Parser(MODEL1, string)

    def test_len_ts_block(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        expected = 3
        actual = len(parsed.ts_blocks)
        self.assertEqual(expected, actual)

    def test_types_ts_block(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        print(parsed.ts_blocks)
        actual = all([isinstance(i, _TimeSeriesBlock) for i in parsed.ts_blocks.values()])
        self.assertTrue(actual)

    def test_ts_block_name(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        ts_block = list(parsed.ts_blocks.values())[0]
        actual = ts_block.name
        expected = 'InsulinOnly'
        self.assertEqual(expected, actual)

    def test_ts_block_args_len(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        ts_block = list(parsed.ts_blocks.values())[0]
        actual = len(ts_block.ts_arg_list)
        self.assertEqual(actual, 3)

    def test_ts_block_arg_list_to_dict(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        ts_block = list(parsed.ts_blocks.values())[0]
        actual = ts_block.ts_arg_list.to_dict()
        expected = {'Insulin': 1.0, 'Rapamycin': 0.0, 'AA': 0.0}
        self.assertEqual(expected, actual)

    def test_ts_block_args(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        ts_block = list(parsed.ts_blocks.values())[0]
        actual = ts_block.ts_arg_list[0].name
        expected = 'Insulin'
        self.assertEqual(expected, actual)

    def test_ts_block_run_timeseries(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        ts_block = list(parsed.ts_blocks.values())[0]
        ts = ts_block.simulate()
        expected = 2.287201
        actual = ts.loc[3.0, 'IRS1a']
        self.assertAlmostEqual(expected, actual, 5)

    def test_obs_block_len(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs_block = parsed.observation_block
        expected = 1
        actual = len(obs_block)
        self.assertEqual(expected, actual)

    def test_obs_block_name(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.name
        expected = 'Obs1'
        self.assertEqual(expected, actual)

    def test_obs_block_operator(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = '>'
        actual = obs.operator
        self.assertEqual(expected, actual)

    def test_obs_clause1(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = Token('NUMBER', 5)
        actual = obs.clause1.clause_elements[0]
        self.assertEqual(expected, actual)

    def test_obs_clause_sum(self):
        obs = 'Obs1: 5 + 6 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = 11
        actual = int(str(obs.clause1.clause_elements[0]))
        self.assertEqual(expected, actual)

    def test_obs_term(self):
        obs = 'Obs1: 4*9 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.clause_elements[0].reduce()
        expected = 36
        self.assertEqual(expected, actual)

    def test_obs_clause_model_entity_reduce(self):
        obs = 'Obs1: Akt[InsulinOnly]@t=0 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = 10.0050015500576
        actual = obs.clause1.clause_elements[0].reduce()
        self.assertEqual(expected, actual)

    def test_obs_term_plus_expression(self):
        obs = 'Obs3: 4*2 +1 > 3'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.clause_elements#.reduce()
        print(actual)
        expected = 9
        # self.assertEqual(expected, actual)

    obs = 'Obs4: 1 - 4*2 > 3'
    obs = 'Obs5: 1 - 4*2 + 6> 3'
    obs = 'Obs6: 1 - 4*2 + 6/2.0 > 3'
    obs = 'Obs7: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=0'
    obs = 'Obs8: Akt[InsulinOnly]@t=0*2 > Akt[InsulinAndRapa]@t=0'
    obs = 'Obs9: 1 + Akt[InsulinOnly]@t=0*2 > Akt[InsulinAndRapa]@t=0'
    obs = 'Obs10: mean Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=0'
    obs = 'Obs11: all Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=0'
    obs = 'Obs12: hyperbolic up Akt[InsulinOnly]'
    obs = 'Obs13: oscillation Akt[InsulinOnly]'
    obs = 'Obs14: sigmoidal down Akt[InsulinOnly]'


if __name__ == '__main__':
    unittest.main()
