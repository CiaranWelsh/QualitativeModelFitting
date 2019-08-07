import unittest

from collections import OrderedDict

from qualitative_model_fitting._parser import Parser


class _RuleTests(unittest.TestCase):

    def setUp(self) -> None:
        self.yaml_input = OrderedDict(
            InsulinOnly=OrderedDict(
                inputs=OrderedDict(
                    Insulin=1,
                    AA=0,
                    Rapamycin=0
                ),
                obs=[
                    'IRS1a > Akt',
                    'IRS1 != PI3Ka',
                    'IRS1@t=35 = Akt@t=65',
                ]
            )
        )

    def test(self):
        input = self.yaml_input['InsulinOnly']['obs']
        p = Parser(input)
        res = p.classify()
        expected = ['always', 'never', 'time']
        self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()
