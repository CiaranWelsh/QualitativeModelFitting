import unittest
from collections import Counter

from ._parser_training import *


class TestDataCreation(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_sample_letters(self):
        ctd = CreateTrainingData(10, seed=42)
        actual = ctd._sample_letters()
        expected = 'ZCoQh_u'
        self.assertEqual(expected, actual)

    def test_sample_time(self):
        ctd = CreateTrainingData(10, seed=42)
        actual = ctd.sample_time()
        expected = 102
        self.assertEqual(expected, actual)

    def test_create_data(self):
        ctd = CreateTrainingData(2, seed=30)
        actual = ctd.create_training_data()
        count = Counter(actual['string'])
        self.assertEqual(count['LTT_mx >= LTT_mx'], 2)
        # self.assertEqual(expected, actual)

    def test_operator_encodings(self):
        ctd = CreateTrainingData(2, seed=1)
        expected = {'>': 2, '<': 3, '>=': 4, '<=': 5, '=': 6, '!>': 7, '!<': 8, '!=': 9}
        self.assertEqual(expected, ctd.operator_encodings)

    def test_preprocess_data(self):
        ctd = CreateTrainingData(6, seed=3)
        df = ctd.create_training_data()
        expected = 18, 5
        actual = df.shape
        self.assertEqual(expected, actual)

    def test_shape(self):
        ctd = CreateTrainingData(100, seed=3)
        df = ctd.create_training_data()
        expected = 100
        actual = df.shape[0]
        self.assertEqual(expected, actual)




if __name__ == '__main__':
    unittest.main()
