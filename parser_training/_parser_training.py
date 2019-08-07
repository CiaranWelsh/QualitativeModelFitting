import nltk
import numpy as np
import pandas as pd
import os, glob, re
import matplotlib.pyplot as plt
import seaborn as sns

from io import StringIO
from string import ascii_letters
from typing import Optional
import tensorflow as tf
from sklearn.utils import shuffle

from sklearn.model_selection import train_test_split

"""
todo think about multi-label classification

"""


class _Base:
    positive_operators = ['>', '<', '>=', '<=', '=']
    negative_operators = ['!>', '!<', '!=']

    operator_offset = 2
    operator_encodings = dict(
        zip(
            positive_operators + negative_operators,
            range(operator_offset, len(positive_operators) + len(negative_operators) + operator_offset)
        )
    )

    not_time_encoding = 0
    time_encoding = 1

    labels = {
        'always': 0,
        'never': 1,
        'time': 2
    }


class CreateTrainingData(_Base):

    def __init__(self, n_instances: int, seed=None, end_time=1000, fname=None) -> None:
        self.n_instances = n_instances
        self.seed = seed
        self.end_time = end_time
        self.fname = fname
        self.create_training_data()

    def _sample_letters(self):
        if self.seed:
            np.random.seed(self.seed)
        word_length = np.random.choice(range(1, 11), )
        ascii = list(ascii_letters) + ['_'] * 10
        sample = np.random.choice(ascii, word_length)
        return ''.join(sample)

    def sample_time(self):
        if self.seed:
            np.random.seed(self.seed)
        return np.random.choice(range(self.end_time))

    def _create_always_data(self, n):
        s = ''
        for i in range(n):
            clause1 = self._sample_letters()
            clause2 = self._sample_letters()
            operator = np.random.choice(self.positive_operators)
            s += f'{clause1} {operator} {clause2}, {self.labels["always"]}\n'
        return s.rstrip()

    def _create_never_data(self, n):
        s = ''
        for i in range(n):
            clause1 = self._sample_letters()
            clause2 = self._sample_letters()
            operator = np.random.choice(self.negative_operators)
            s += f'{clause1} {operator} {clause2}, {self.labels["never"]}\n'
        return s.rstrip()

    def _create_time_data(self, n):
        s = ''
        for i in range(n):
            clause1 = self._sample_letters()
            time1 = self.sample_time()
            clause2 = self._sample_letters()
            time2 = self.sample_time()
            positive_or_negative = np.random.uniform(0, 1)
            sign = self.negative_operators
            if positive_or_negative > 0.5:
                sign = self.positive_operators
            operator = np.random.choice(sign)
            s += f'{clause1}@{time1} {operator} {clause2}@{time2}, {self.labels["time"]}\n'
        return s.rstrip()

    def _create_multiplier_data(self):
        """
        skip this for now
        :return:
        """
        pass

    def create_training_data(self):

        always = self._create_always_data(self.n_instances)
        never = self._create_never_data(self.n_instances)
        time = self._create_time_data(self.n_instances)
        data = f'{always}\n{never}\n{time}'

        cols = ['string', 'label']
        data = pd.read_csv(StringIO(data), header=None)
        data.columns = cols

        enc = Encoder()
        data = enc.encode(data)

        if self.fname:
            data.to_csv(self.fname)

        data = shuffle(data)
        return data.reset_index()


class Encoder(_Base):

    def __init__(self):
        pass

    def encode(self, data):
        strings = data['string'].values
        new_strings = []
        clause_1s = []
        operators = []
        clause_2s = []
        for string in strings:
            clause1, operator, clause2 = string.split(' ')
            if '@' in clause1 and '@' in clause2:
                clause_encoding = self.time_encoding
            else:
                clause_encoding = self.not_time_encoding
            operator_encoding = self.operator_encodings[operator]

            new_strings.append(f'{clause_encoding} {operator_encoding} {clause_encoding}')
            clause_1s.append(clause_encoding)
            clause_2s.append(clause_encoding)
            operators.append(operator_encoding)

        df2 = pd.DataFrame([clause_1s, operators, clause_2s]).transpose()
        df2.columns = ['clause1', 'operator', 'clause2']
        df = pd.concat([data, df2], axis=1)
        return df


if __name__ == '__main__':

    WD = os.path.dirname(__file__)
    DATA_DIR = os.path.join(WD, 'data')
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    DATA_FILE = os.path.join(DATA_DIR, 'data.csv')
    TEST_DATA_FILE = os.path.join(DATA_DIR, 'test_data.csv')
    TRAIN_DATA_FILE = os.path.join(DATA_DIR, 'train_data.csv')
    VAL_DATA_FILE = os.path.join(DATA_DIR, 'val_data.csv')
    MODEL_PATH = os.path.join(DATA_DIR, 'nn_model.h5')

    # Create dataset
    CREATE_DATA = True

    # retrain model
    OVERWRITE_MODEL = True

    # train sequential model
    TRAIN_MODEL = True


    if CREATE_DATA:
        train = CreateTrainingData(10000, fname=TRAIN_DATA_FILE)
        test = CreateTrainingData(1000, fname=TEST_DATA_FILE)
        val = CreateTrainingData(2000, fname=VAL_DATA_FILE)

    if TRAIN_MODEL:
        train_data = pd.read_csv(TRAIN_DATA_FILE, index_col=0)
        test_data = pd.read_csv(TEST_DATA_FILE, index_col=0)
        val_data = pd.read_csv(VAL_DATA_FILE, index_col=0)

        print(train_data)

        features = ['clause1', 'operator', 'clause2']

        train_labels = train_data['label']
        test_labels = test_data['label']
        val_labels = val_data['label']

        train_data = train_data[features]
        test_data = test_data[features]
        val_data = val_data[features]

        if not os.path.isfile(MODEL_PATH) or OVERWRITE_MODEL:

            model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, input_shape=(train_data.shape[1],), activation='relu'),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dense(3, activation='softmax'),
            ])
            model.compile(
                optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['acc']
            )
            history = model.fit(train_data, train_labels, batch_size=100, epochs=100,
                      validation_data=(val_data, val_labels))

            print(history.history.keys())

            plt.figure()
            for k, v in history.history.items():
                plt.plot(v, label=k)
            plt.legend()
            plt.show()

            model.save(MODEL_PATH)

        else:
            model = tf.keras.models.load_model(MODEL_PATH)

        results = model.evaluate(test_data, test_labels, batch_size=50)
        print(results)
        results = model.predict(test_data)
        test_results = pd.DataFrame(results)
        print(test_results.idxmax(1))









