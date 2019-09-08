import unittest

from qualitative_model_fitting._parser import Parser

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
"""

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()

    def do_tst(self, obs):
        string = STRING + obs
        expected = """start
  block
    InsulinOnly
    ts_arg_list
      ts_arg
        Insulin
        1
      ts_arg
        Rapamycin
        0
      ts_arg
        AA
        0
    0
    100
    101
  block
    InsulinAndRapa
    ts_arg_list
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
    InsulinAndRapaAndAA
    ts_arg_list
      ts_arg
        Insulin
        1
      ts_arg
        Rapamycin
        1
      ts_arg
        AA
        1.0
    0
    100
    101
  block
    observation_block
      statement
        Obs1
        clause1
          model_entity
            Akt
            Insulin
            0
        >
        clause2
          model_entity
            Akt
            InsulinAndRapa
            10
      statement
        Obs2
        clause1
          mean
          model_entity
            Akt
            Insulin
            (0,100)
        >
        clause2
          model_entity
            Akt
            InsulinAndRapa
            10
      statement
        Obs3
        clause1
          all
          model_entity
            Akt
            InsulinAndRapa
            (0, 100)
        ==
        clause2
          expression	0"""
        actual = self.parser.pretty(string)
        print(actual)
        # self.assertEqual(expected.strip(), actual.strip())

    def get_statement(self, obs):
        string = STRING + 'observation\n\t' + obs
        parsed = self.parser.parse(string)
        parsed = parsed.find_data('statement')
        parsed = [i for i in parsed]
        return parsed

    def test1(self):
        obs = 'Obs1: 4 > 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs1'), Tree(clause1, [Token(NUMBER, '4')]), Token(OPERATOR, '>'), Tree(clause2, [Token(NUMBER, '3')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test2(self):
        obs = 'Obs2: 4*2 > 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs2'), Tree(clause1, [Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')])]), Token(OPERATOR, '>'), Tree(clause2, [Token(NUMBER, '3')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test3(self):
        obs = 'Obs3: 4*2 +1 > 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs3'), Tree(clause1, [Tree(expression, [Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')]), Token(ADD, '+'), Token(NUMBER, '1')])]), Token(OPERATOR, '>'), Tree(clause2, [Token(NUMBER, '3')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test4(self):
        obs = 'Obs4: 1 - 4*2 > 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs4'), Tree(clause1, [Tree(expression, [Token(NUMBER, '1'), Token(SUB, '-'), Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')])])]), Token(OPERATOR, '>'), Tree(clause2, [Token(NUMBER, '3')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test5(self):
        obs = 'Obs5: 1 - 4*2 + 6> 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs5'), Tree(clause1, [Tree(expression, [Token(NUMBER, '1'), Token(SUB, '-'), Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')]), Token(ADD, '+'), Token(NUMBER, '6')])]), Token(OPERATOR, '>'), Tree(clause2, [Token(NUMBER, '3')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test6(self):
        obs = 'Obs6: 1 - 4*2 + 6/2.0 > 3'
        parsed = self.get_statement(obs)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs6'), Tree(clause1, [Tree(expression, [Token(NUMBER, '1'), Token(SUB, '-'), Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')]), Token(ADD, '+'), Tree(term, [Token(NUMBER, '6'), Token(DIV, '/'), Token(NUMBER, '2.0')])])]), Token(OPERATOR, '>'), Tree(clause2, [Token(NUMBER, '3')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)





if __name__ == '__main__':
    unittest.main()
