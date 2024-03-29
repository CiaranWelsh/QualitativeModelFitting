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

    def test_obs_block_name2(self):
        obs = 'Obs1: 5 < 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.name
        expected = 'Obs1'
        self.assertEqual(expected, actual)

    def test_obs_block_operator_gt(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = str(obs.operator)
        self.assertEqual('>', actual)

    def test_obs_block_operator_ne(self):
        obs = 'Obs1: 5 != 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = '!='
        actual = str(obs.operator)
        self.assertEqual(expected, actual)

    def test_obs_block_operator_ge(self):
        obs = 'Obs1: 5 >= 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = str(obs.operator)
        self.assertEqual('>=', actual)

    def test_obs_clause1(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = '5'
        actual = str(obs.clause1.reduce())
        self.assertEqual(expected, actual)

    def test_obs_clause_is_time_interval(self):
        obs = 'Obs1: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        self.assertFalse(obs.clause1.is_time_interval())

    def test_obs_clause_is_time_interval2(self):
        obs = 'Obs1: Akt[InsulinOnly]@t=(0, 5) > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        self.assertTrue(obs.clause1.is_time_interval())

    def test_obs_clause_sum(self):
        obs = 'Obs1: 5 + 6 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = 11
        actual = int(str(obs.clause1.reduce()))
        self.assertEqual(expected, actual)

    def test_obs_term(self):
        obs = 'Obs1: 4*9 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()
        expected = 36
        self.assertEqual(expected, actual)

    def test_obs_clause_model_entity_reduce(self):
        obs = 'Obs1: Akt[InsulinOnly]@t=0 > 6'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        expected = 10.0050015500576
        actual = obs.clause1.reduce()
        self.assertEqual(expected, actual)

    def test_obs_term_plus_expression(self):
        obs = 'Obs3: 4*2 +1 > 3'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()  # .reduce()
        expected = 9
        print(type(actual))
        self.assertEqual(expected, int(str(actual)))

    def test_obs_term_plus_expression2(self):
        obs = 'Obs4: 1 - 4*2 > 3'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()  # .reduce()
        expected = -7
        self.assertEqual(expected, int(str(actual)))

    def test_obs_term_plus_expression3(self):
        obs = 'Obs5: 1 - 4*2 + 6 > 3'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()  # .reduce()
        expected = -1
        self.assertEqual(expected, int(str(actual)))

    def test_obs_term_plus_expression4(self):
        obs = 'Obs6: 1 - 4*2 + 6/2.0 > 3'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()  # .reduce()
        expected = -4.0
        self.assertEqual(expected, float(str(actual)))

    def test_obs_model_entity(self):
        obs = 'Obs7: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()
        expected = 10.0050015500576
        self.assertEqual(expected, actual)

    def test_obs_model_entity_with_term(self):
        obs = 'Obs8: Akt[InsulinOnly]@t=0*2 > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()
        expected = 20.0100031001152
        self.assertEqual(expected, actual)

    def test_obs_model_entity_with_expression_and_term(self):
        obs = 'Obs9: 1 + Akt[InsulinOnly]@t=0*2 > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block[0]
        actual = obs.clause1.reduce()
        expected = 21.0100031001152
        self.assertEqual(expected, actual)

    def test_obs_statement_reduce(self):
        obs = 'Obs: 5 > 6'
        parsed = self.get_parsed_observatoin(obs)
        self.assertFalse(parsed.observation_block[0].reduce())

    def test_obs_model_entity_with_interval_time_and_all_func(self):
        obs = 'Obs10: all(Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=1)'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block
        actual = obs[0].reduce()
        self.assertFalse(actual)

    def test_obs_model_entity_with_interval_time_and_any_func(self):
        obs = 'Obs10: any(Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=1)'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block
        actual = obs[0].reduce()
        self.assertTrue(actual)

    def test_obs_model_entity_with_interval_time_and_mean_func(self):
        obs = 'Obs10: mean(Akt[InsulinOnly]@t=(0, 5)) > Akt[InsulinAndRapa]@t=1'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block
        expected = 7.632460576669665
        actual = obs[0].clause1.reduce()
        self.assertEqual(expected, actual)

    def test_obs_model_entity_with_interval_time_and_max(self):
        obs = 'Obs11: max(Akt[InsulinOnly]@t=(0, 5)) == max(Akt[InsulinAndRapa]@t=(0,5))'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block
        actual = obs[0].reduce()
        self.assertTrue(actual)

    def test_obs_model_entity_with_interval_all(self):
        obs = 'Obs12: all(pS6K[InsulinOnly]@t=(0, 100) >= pS6K[InsulinAndRapa]@t=(0, 100))'
        parsed = self.get_parsed_observatoin(obs)
        obs = parsed.observation_block
        actual = str(obs[0])
        expected = 'all(TimeInterval >= TimeInterval)'
        self.assertEqual(expected, actual)




if __name__ == '__main__':
    unittest.main()
