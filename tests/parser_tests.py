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
                    'IRS1a > Akt'
                ]
            )
        )

    def rule_test_helper(self, rule, expected):
        """
        will test that rule is of type expected.
        :return:
        """
        p = Parser(rule)
        cls = p._dispatch()
        actual = cls[1].__class__.__name__
        self.assertEqual(expected, actual)

    def test_always_rule(self):
        expected = '_AlwaysRule'
        rule = 'IRS1a > Akt'
        self.rule_test_helper(rule, expected)

    def test_never_rule(self):
        rule = 'IRS1a !> Akt'
        expected = '_NeverRule'
        self.rule_test_helper(rule, expected)

    def test_time_rule(self):
        rule = 'IRS1a@t=3 > Akt@t=3'
        expected = '_TimeRule'
        self.rule_test_helper(rule, expected)















if __name__ == '__main__':
    unittest.main()











