import unittest
from collections import Counter

from parser_training._parser_training import *
from qualitative_model_fitting import Encoder


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
        actual = ctd._sample_time()
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
        actual = ctd._sample_time()
        expected = 102
        self.assertEqual(expected, actual)

    def test_create_data(self):
        pass

    def test_create_clause(self):
        ctd = CreateTrainingData(2, seed=6)
        expected = ('JuQTpQqzbl@t=(906,906)/7.17', {'point': 0, 'interval': 1, 'fun': 0, '_const': 0, 'expression': 1})
        actual = ctd._create_clause()
        self.assertEqual(expected, actual)

    def test_create_data(self):
        ctd = CreateTrainingData(2, seed=3)
        x = ctd.create_data()
        expected = '_d_iav_tk@t=874*0.71'
        actual = x.loc[0, 'clause']
        self.assertEqual(expected, actual)

    def test_create_data2(self):
        ctd = CreateTrainingData(2, seed=3)
        # build an encoder and decoder to convert strings into numerical sequences of equal length.
        # x = ctd.create_data()
        # expected = '_d_iav_tk@t=874*0.71'
        # actual = x.loc[0, 'clause']
        # self.assertEqual(expected, actual)

    def test_label_Data(self):
        ctd = CreateTrainingData(5, seed=7)
        x = ctd.label_data(ctd.create_data())
        self.assertTrue('label' in x.columns)


class EncoderTests(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_encoder_mean(self):
        string = 'mean IRS1@t=(0, 100) > mean IRS1a@t=(0, 100)'
        encoder = Encoder(string)
        expected = [2, 3, 1, 5, 6, 2, 3, 1, 5]
        actual = encoder.encode()
        self.assertListEqual(expected, actual)

    def test_encoder_all(self):
        string = 'all IRS1@t=(0, 100) > all IRS1a@t=(0, 100)'
        encoder = Encoder(string)
        expected = [2, 3, 1, 5, 6, 2, 3, 1, 5]
        actual = encoder.encode()
        self.assertListEqual(expected, actual)

    def test_encoder_min(self):
        string = 'min IRS1@t=(0, 100) > min IRS1a@t=(0, 100)'
        encoder = Encoder(string)
        expected = [2, 3, 1, 5, 6, 2, 3, 1, 5]
        actual = encoder.encode()
        self.assertListEqual(expected, actual)

    def test_encoder_max(self):
        string = 'max IRS1@t=(0, 100) > max IRS1a@t=(0, 100)'
        encoder = Encoder(string)
        expected = [2, 3, 1, 5, 6, 2, 3, 1, 5]
        actual = encoder.encode()
        self.assertListEqual(expected, actual)

    def test_encoder_interval(self):
        string = 'A@t=(0, 10) == B@t=4'
        enc = Encoder(string)
        expected = [3, 1, 5, 6, 3, 1, 4]
        actual = enc.encode()
        self.assertListEqual(expected, actual)

    def test_encoder_interval(self):
        string = 'A@t=(0, 10) == B@t=4 / 2'
        enc = Encoder(string)
        expected = [3, 1, 5, 6, 3, 1, 7, 4]
        actual = enc.encode()
        self.assertListEqual(expected, actual)

    def test_encoder_random1(self):
        string = '_X@t=(468,925)**43 <= all Ba@t=(498,704)'
        enc = Encoder(string)
        expected = [3, 1, 5, 7, 4, 6, 2, 3, 1, 5]
        actual = enc.encode()
        self.assertEqual(expected, actual)

    def test_dispatch(self):
        encoder = Encoder(self.mean_string)
        encoder._encode_part()


class CreateDataTests(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_create_clause(self):
        td = CreateTrainingData(2, seed=4)
        expected = ('87-fbOxiYj_@t=(122,122)', 5)
        actual = td._create_clause()
        self.assertEqual(expected, actual)

    def test_create_data(self):
        td = CreateTrainingData(2, seed=5)
        expected = 'oV_M@t=867 != oV_M@t=867'
        actual = td.create_data().iloc[0, 0]
        print(td.create_data())
        self.assertEqual(expected, actual)

    def test(self):
        pass

    # def test_decoder(self):
    #     d = Decoder()
    #     x = d.decode(102105111101)
    #     expected = "(['interval', 'expression'], '!=', ['point'])"
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
