import unittest

from collections import OrderedDict
from tests import TEST_INPUT1

from qualitative_model_fitting._parser import _Parser


class RuleTests(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_encoder(self):
        input = TEST_INPUT1['InsulinOnly']['obs']
        p = _Parser(input)
        actual = p.statements.iloc[:3, 1].tolist()
        expected = [
            [3, 6, 3], [3, 6, 3], [3, 1, 4, 6, 3, 1, 4]
        ]
        self.assertEqual(expected, actual)

def suite():
    s = unittest.TestSuite()
    s.addTest(RuleTests())
    return s

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())



