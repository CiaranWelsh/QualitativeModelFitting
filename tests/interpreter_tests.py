import unittest

import numpy as np

from qualitative_model_fitting._parser import Parser
from qualitative_model_fitting._interpreter import _Clause, _ModelEntity, _Operator, _Statement, Interpreter

from tests import MODEL1


class TestInterpreter(unittest.TestCase):

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
              Obs2: mean Akt[InsulinOnly]@t=(0, 100) > Akt[InsulinAndRapa]@t=10
              Obs3: Akt[InsulinOnly]@t=0 == Akt[InsulinAndRapa]@t=0
              Obs4: all Akt[InsulinAndRapa]@t=(0, 100) == 0
              Obs5: Akt[InsulinAndRapa]@t=15*2 == 4.5 + Akt[InsulinOnly]@t=15

          """
        parser = Parser()
        self.tree = parser.parse(string)

    def test_timeseries_block(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        actual = ts
        expected = [{'name': 'InsulinOnly', 'conditions': {'Insulin': 1.0, 'Rapamycin': 0.0, 'AA': 0.0}, 'integration_settings': {'start': 0.0, 'stop': 100.0, 'step': 101.0}}, {'name': 'InsulinAndRapa', 'conditions': {'Insulin': 1.0, 'Rapamycin': 1.0}, 'integration_settings': {'start': 0.0, 'stop': 100.0, 'step': 101.0}}, {'name': 'InsulinAndRapaAndAA', 'conditions': {'Insulin': 1.0, 'Rapamycin': 1.0, 'AA': 0.3}, 'integration_settings': {'start': 0.0, 'stop': 100.0, 'step': 101.0}}]
        # self.assertEqual(expected, actual)
        print(ts)

    def test_statement_name(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        expected = 'Obs1'
        actual = obs[0].name
        self.assertEqual(expected, actual)

    def test_clause1(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        self.assertIsInstance(obs[0].clause1, _Clause)

    def test_clause2(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()

        self.assertIsInstance(obs[0].clause2, _Clause)

    def test_operator(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        expected = '>'
        actual = obs[0].operator
        self.assertEqual(expected, actual)

    def test_clause_modifier_obs1(self):
        i = Interpreter(self.tree)
        ts, obs = i.interpret()
        clause = obs[0].clause1
        self.assertIsNone(clause.modifier)

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


if __name__ == '__main__':
    unittest.main()
