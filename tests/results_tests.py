import unittest

from qualitative_model_fitting._results import PandasResult, DictResults


class BaseResultTests(unittest.TestCase):

    def test_add_condition_keys(self):
        result = DictResults()
        condition_name = 'test_condition'
        result.add_condition(condition_name)
        actual = list(result.keys())[0]
        self.assertEqual(actual, condition_name)

    def test_add_condition_values(self):
        result = DictResults()
        condition_name = 'test_condition'
        result.add_condition(condition_name)
        actual = list(result.values())[0]
        self.assertEqual(actual, {})

    def test_result_contains(self):
        result = DictResults()
        condition_name = 'test_condition'
        result.add_condition(condition_name)
        self.assertIn('test_condition', result)

    def test_getitem(self):
        result = DictResults()
        condition_name = 'test_condition'
        result.add_condition(condition_name)
        expected = {}
        actual = result['test_condition']
        self.assertEqual(expected, actual)

    def test_setitem(self):
        result = DictResults()
        result['test_condition'] = {}
        expected = {}
        actual = result['test_condition']
        self.assertEqual(expected, actual)

    def test_items(self):
        result = DictResults()
        result['test_condition'] = {}
        expected = [('test_condition', {})]
        actual = list(result.items())
        self.assertEqual(expected, actual)


class PandasResultsTests(unittest.TestCase):

    def test(self):
        result = PandasResult()
        obs = [
            'X@t=4 > X@t=6',
            'X@t=8 > X@t=10',
        ]
        result.obs['test_condition'] = obs
        result['test_condition'] = {}
        print(result._make_dataframe())


if __name__ == '__main__':
    unittest.main()
