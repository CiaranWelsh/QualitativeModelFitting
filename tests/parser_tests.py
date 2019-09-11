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
        steadystate ss1 {Insulin=1}
"""

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()

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
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs1'), Token(NUMBER, '4'), Token(OPERATOR, '>'), Token(NUMBER, '3')])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test2(self):
        obs = 'Obs2: 4*2 > 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs2'), Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')]), Token(OPERATOR, '>'), Token(NUMBER, '3')])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test3(self):
        obs = 'Obs3: 4*2 +1 > 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs3'), Tree(expression, [Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')]), Token(ADD, '+'), Token(NUMBER, '1')]), Token(OPERATOR, '>'), Token(NUMBER, '3')])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test4(self):
        obs = 'Obs4: 1 - 4*2 > 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs4'), Tree(expression, [Token(NUMBER, '1'), Token(SUB, '-'), Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')])]), Token(OPERATOR, '>'), Token(NUMBER, '3')])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test5(self):
        obs = 'Obs5: 1 - 4*2 + 6> 3'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs5'), Tree(expression, [Token(NUMBER, '1'), Token(SUB, '-'), Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')]), Token(ADD, '+'), Token(NUMBER, '6')]), Token(OPERATOR, '>'), Token(NUMBER, '3')])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test6(self):
        obs = 'Obs6: 1 - 4*2 + 6/2.0 > 3'
        parsed = self.get_statement(obs)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs6'), Tree(expression, [Token(NUMBER, '1'), Token(SUB, '-'), Tree(term, [Token(NUMBER, '4'), Token(MUL, '*'), Token(NUMBER, '2')]), Token(ADD, '+'), Tree(term, [Token(NUMBER, '6'), Token(DIV, '/'), Token(NUMBER, '2.0')])]), Token(OPERATOR, '>'), Token(NUMBER, '3')])]"
        actual = str(parsed)
        print(parsed)
        self.assertEqual(expected, actual)

    def test7(self):
        obs = 'Obs7: Akt[InsulinOnly]@t=0 > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs7'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinOnly'), Token(POINT_TIME, '0')]), Token(OPERATOR, '>'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinAndRapa'), Token(POINT_TIME, '0')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test8(self):
        obs = 'Obs8: Akt[InsulinOnly]@t=0*2 > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs8'), Tree(term, [Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinOnly'), Token(POINT_TIME, '0')]), Token(MUL, '*'), Token(NUMBER, '2')]), Token(OPERATOR, '>'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinAndRapa'), Token(POINT_TIME, '0')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test9(self):
        obs = 'Obs9: 1 + Akt[InsulinOnly]@t=0*2 > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_statement(obs)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs9'), Tree(expression, [Token(NUMBER, '1'), Token(ADD, '+'), Tree(term, [Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinOnly'), Token(POINT_TIME, '0')]), Token(MUL, '*'), Token(NUMBER, '2')])]), Token(OPERATOR, '>'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinAndRapa'), Token(POINT_TIME, '0')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test10(self):
        obs = 'Obs10: mean Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_statement(obs)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs10'), Tree(clause1, [Token(FUNC, 'mean'), Tree(model_entity, [Token(SYMBOL, 'Akt'), Token(CONDITION, 'InsulinOnly'), Token(INTERVAL_TIME, '(0, 5)')])]), Token(OPERATOR, '>'), Tree(clause2, [Tree(model_entity, [Token(SYMBOL, 'Akt'), Token(CONDITION, 'InsulinAndRapa'), Token(POINT_TIME, '0')])])])]"
        actual = str(parsed)
        print(parsed)
        # self.assertEqual(expected, actual)

    def test11(self):
        obs = 'Obs11: all Akt[InsulinOnly]@t=(0, 5) > Akt[InsulinAndRapa]@t=0'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs11'), Tree(clause1, [Token(FUNC, 'all'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinOnly'), Token(INTERVAL_TIME, '(0, 5)')])]), Token(OPERATOR, '>'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinAndRapa'), Token(POINT_TIME, '0')])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test12(self):
        obs = 'Obs12: hyperbolic up Akt[InsulinOnly]'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs12'), Tree(qual_exp, [Token(SHAPE, 'hyperbolic'), Token(DIRECTION, 'up'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinOnly')])])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test13(self):
        obs = 'Obs13: oscillation Akt[InsulinOnly]'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs13'), Tree(qual_exp, [Token(SHAPE, 'oscillation'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinOnly')])])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)

    def test14(self):
        obs = 'Obs14: sigmoidal down Akt[InsulinOnly]'
        parsed = self.get_statement(obs)
        print(parsed)
        expected = "[Tree(statement, [Token(OBS_NAME, 'Obs14'), Tree(qual_exp, [Token(SHAPE, 'sigmoidal'), Token(DIRECTION, 'down'), Tree(model_entity, [Token(NAME, 'Akt'), Token(CONDITION, 'InsulinOnly')])])])]"
        actual = str(parsed)
        self.assertEqual(expected, actual)





if __name__ == '__main__':
    unittest.main()
