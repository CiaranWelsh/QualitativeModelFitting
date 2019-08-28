import unittest

from tests import TEST_INPUT1

from qualitative_model_fitting._parser import _Parser


class ParserTests(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_encoder(self):
        input = TEST_INPUT1['InsulinOnly']['obs']
        p = _Parser(input)
        actual = p.statements.iloc[:3, 1].tolist()
        print(actual)
        expected = [[3, 1, 4, 6, 3, 1, 4], [3, 1, 4, 6, 3, 1, 4], [2, 3, 1, 5, 7, 4, 6, 4]]
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()



