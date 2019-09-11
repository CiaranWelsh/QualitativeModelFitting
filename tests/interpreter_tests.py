import unittest

import numpy as np

from qualitative_model_fitting._parser import Parser, _Observation, _Clause, _ModelEntity, _Operator
from qualitative_model_fitting._interpreter import Interpreter

from tests import MODEL1


class TestInterpreter(unittest.TestCase):

    def setUp(self) -> None:
        self.ts_string = """
        timeseries InsulinOnly {
          Insulin=1, Rapamycin=0, AA=0
        } 0, 100, 101
        timeseries InsulinAndRapa {
          Insulin=1, Rapamycin=1
        } 0, 100, 101
        timeseries InsulinAndRapaAndAA {
          Insulin=1, Rapamycin=1, AA=0.3
        } 0, 100, 101
        
        //observation 
        //    Obs1: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=10
        //    Obs2: mean Akt[InsulinOnly]@t=(0, 100) > Akt[InsulinAndRapa]@t=10
        //    Obs3: Akt[InsulinOnly]@t=0 == Akt[InsulinAndRapa]@t=0
        //    Obs4: all Akt[InsulinAndRapa]@t=(0, 100) == 0
        //    Obs5: Akt[InsulinAndRapa]@t=15*2 == 4.5 + Akt[InsulinOnly]@t=15

        """

    def test_timeseries_block(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        actual = ts
        expected = [{'name': 'InsulinOnly', 'conditions': {'Insulin': 1.0, 'Rapamycin': 0.0, 'AA': 0.0},
                     'integration_settings': {'start': 0.0, 'stop': 100.0, 'step': 101.0}},
                    {'name': 'InsulinAndRapa', 'conditions': {'Insulin': 1.0, 'Rapamycin': 1.0},
                     'integration_settings': {'start': 0.0, 'stop': 100.0, 'step': 101.0}},
                    {'name': 'InsulinAndRapaAndAA', 'conditions': {'Insulin': 1.0, 'Rapamycin': 1.0, 'AA': 0.3},
                     'integration_settings': {'start': 0.0, 'stop': 100.0, 'step': 101.0}}]
        self.assertEqual(expected, actual)

    def test_statement_name(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        expected = 'Obs1'
        actual = obs[0].name
        self.assertEqual(expected, actual)

    def test_clause1(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        print(obs)
        # self.assertIsInstance(obs[0].clause1, _Clause)

    def test_clause2(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        print(obs[0])
        self.assertIsInstance(obs[0].clause2, _Clause)

    def test_operator(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        expected = '>'
        actual = obs[0].operator
        self.assertEqual(expected, actual)

    def interpreter(self, obs, print_string=False):
        string = self.ts_string + 'observation\n\t\t\t' + obs
        if print_string:
            print(string)
        parser = Parser()
        tree = parser.parse(string)
        i = Interpreter(tree)
        return i.interpret()

    def test_clause_modifier_obs1(self):
        obs_string = 'Obs1: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=10'
        self.interpreter(obs_string)
        # ts, obs = self.interpreter(obs_string)
        # print(obs)
        # clause = obs[0].clause1
        # print(clause)
        # self.assertIsNone(clause.modifier)

    def test_clause_modifier_obs2(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        clause = obs[1].clause1
        expected = np.mean
        actual = clause.modifier
        self.assertEqual(expected, actual)

    def test_model_entity_name(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        clause = obs[1].clause1
        entity = clause.model_entity
        expected = 'Akt'
        actual = entity.component_name
        self.assertEqual(expected, actual)

    def test_model_entity_condition(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        clause = obs[1].clause1
        entity = clause.model_entity
        expected = 'InsulinOnly'
        actual = entity.condition
        self.assertEqual(expected, actual)

    def test_model_entity_time(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        clause = obs[1].clause1
        entity = clause.model_entity
        expected = '(0, 100)'
        actual = entity.time
        self.assertEqual(expected, actual)

    def test_model_entity_time2(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        clause = obs[1].clause2
        entity = clause.model_entity
        expected = '10'
        actual = entity.time
        self.assertEqual(expected, actual)

    def test_operator(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        op = obs[1].operator
        import operator
        expected = operator.gt
        actual = op.operator
        self.assertEqual(expected, actual)

    def test_entity_str(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        expected = 'Akt[InsulinOnly]@t=0'
        actual = str(obs[0].clause1.model_entity)
        self.assertEqual(expected, actual)

    def test_clause_str(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        expected = 'mean Akt[InsulinOnly]@t=(0, 100)'
        actual = str(obs[1].clause1)
        self.assertEqual(expected, actual)

    def test_statement_str(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        expected = 'Obs2: mean Akt[InsulinOnly]@t=(0, 100) > Akt[InsulinAndRapa]@t=10'
        actual = str(obs[1])
        self.assertEqual(expected, actual)

    def test(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        print(obs[4])
        import logging
        print('x', logging.root.manager.loggerDict)


if __name__ == '__main__':
    unittest.main()

'''
clause 
    - expression
        - model_entity
        - numerical operation
    - function 
    - model_entity
'''
