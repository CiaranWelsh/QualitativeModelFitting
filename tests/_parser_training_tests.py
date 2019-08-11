import unittest
from collections import Counter

from parser_training._parser_training import *


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
        print(actual)
        count = Counter(actual['rule'])
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
        expected = 300
        actual = df.shape[0]
        self.assertEqual(expected, actual)


class TestDataCreation2(unittest.TestCase):

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
        pass

    def test_create_clause(self):
        ctd = CreateTrainingData(2, seed=6)
        expected = ('JuQTpQqzbl@t=(906,906)/7.17', {'point': 0, 'range': 1, 'fun': 0, 'const': 0, 'expression': 1})
        actual = ctd.create_clause()
        self.assertEqual(expected, actual)

    def test_create_data(self):
        ctd = CreateTrainingData(2, seed=3)
        x = ctd.create_data()
        expected = '_d_iav_tk@t=874*0.71'
        actual = x.loc[0, 'clause']
        self.assertEqual(expected, actual)

    def test_create_data2(self):
        ctd = CreateTrainingData(2, seed=3)
        build an encoder and decoder to convert strings into numerical sequences of equal length. 
        # x = ctd.create_data()
        # expected = '_d_iav_tk@t=874*0.71'
        # actual = x.loc[0, 'clause']
        # self.assertEqual(expected, actual)

    def test_label_Data(self):
        ctd = CreateTrainingData(5, seed=7)
        x = ctd.label_data(ctd.create_data())
        self.assertTrue('label' in x.columns)



    # def test_decoder(self):
    #     d = Decoder()
    #     x = d.decode(102105111101)
    #     expected = "(['range', 'expression'], '!=', ['point'])"
    #     actual = str(x)
    #     self.assertEqual(expected, actual)

    # def test_operator_encodings(self):
    #     ctd = CreateTrainingData(2, seed=1)
    #     expected = {'>': 2, '<': 3, '>=': 4, '<=': 5, '=': 6, '!>': 7, '!<': 8, '!=': 9}
    #     self.assertEqual(expected, ctd.operator_encodings)
    #
    # def test_preprocess_data(self):
    #     ctd = CreateTrainingData(6, seed=3)
    #     df = ctd.create_training_data()
    #     expected = 18, 5
    #     actual = df.shape
    #     self.assertEqual(expected, actual)
    #
    # def test_shape(self):
    #     ctd = CreateTrainingData(100, seed=3)
    #     df = ctd.create_training_data()
    #     expected = 300
    #     actual = df.shape[0]
    #     self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
