import unittest

from tests import MODEL1, TEST_INPUT1
from qualitative_model_fitting._test_factory import TestCase
from qualitative_model_fitting._simulator import TimeSeries


class TestTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.name = list(TEST_INPUT1.keys())[0]
        self.data = TimeSeries(MODEL1, TEST_INPUT1, 0, 100, 101).simulate()
        self.obs = TEST_INPUT1[self.name]['obs']

    def test_dynamic_class_creation_point_to_point0(self):
        statement = 'IRS1a@t=10 > Akt@t=10'
        self.cls = type(self.name, (TestCase,), {'data': self.data['InsulinOnly'], 'obs': statement})
        methods = self.cls().make_test()
        test_method = methods['test_statement_0']
        test_data = self.data['InsulinOnly'][['IRS1a', 'Akt']].loc[10.0]
        expected = test_data['IRS1a'] > test_data['Akt']
        actual = test_method(self.cls)
        self.assertTrue(expected, actual)

    def test_dynamic_class_creation_point_to_point1(self):
        statement = 'IRS1@t=35 == Akt@t=65'
        print(self.obs[1])
        self.cls = type(self.name, (TestCase,), {'data': self.data['InsulinOnly'], 'obs': statement})
        methods = self.cls().make_test()
        test = methods['test_statement_0']
        actual = test(self.cls)
        test_data = self.data['InsulinOnly'][['IRS1', 'Akt']]
        irs1 = test_data['IRS1'].loc[35]
        akt = test_data['Akt'].loc[65]
        expected = irs1 == akt  # eval to false
        self.assertEqual(expected, actual)

    def test_dynamic_class_creation_point_to_interval_with_all(self):
        statement = 'IRS1@t=25 != all IRS1@t=(25,35)'
        self.cls = type(self.name, (TestCase,), {'data': self.data['InsulinOnly'], 'obs': statement})
        methods = self.cls().make_test()
        test = methods['test_statement_0']
        c1 = float(self.data['InsulinOnly']['IRS1'].loc[25])
        c2 = self.data['InsulinOnly']['IRS1'].loc[25:35, ]
        expected = c1 != c2.all()
        actual = test(self.cls)
        self.assertEqual(expected, actual)

    def test_dynamic_class_expression1(self):
        statement = 'sum IRS1@t=(10,15) - 10 != 94'
        self.cls = type(self.name, (TestCase,), {'data': self.data['InsulinOnly'], 'obs': statement})
        methods = self.cls().make_test()
        test = methods['test_statement_0']
        test(self.cls)
        c1 = self.data['InsulinOnly']['IRS1'].loc[10:15, ]
        c1 = c1.sum()
        c2 = 94
        self.assertNotEqual(c1, c2)

        # expected = c1 != c2.all()
        # actual = test(self.cls)
        # self.assertEqual(expected, actual)

        # actual = test(self.cls)
        # test_data = self.data['InsulinOnly'][['IRS1', 'Akt']]
        # irs1 = test_data['IRS1'].loc[35]
        # akt = test_data['Akt'].loc[65]
        # expected = irs1 == akt #eval to false
        # self.assertEqual(expected, actual)
        #
        #
        # # self.assertTrue(callable(x))


if __name__ == '__main__':
    unittest.main()
