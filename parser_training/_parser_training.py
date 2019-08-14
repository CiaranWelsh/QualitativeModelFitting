import numpy as np
import pandas as pd
import os, glob, re
import matplotlib.pyplot as plt
import seaborn as sns

from copy import deepcopy
from time import time
from io import StringIO
from string import ascii_letters
from typing import Optional
import tensorflow as tf
from functools import reduce
from itertools import combinations, permutations

from sklearn.utils import shuffle

from sklearn.model_selection import train_test_split

# todo think about multi-label classification

"""
Create a keras model for classifying rules (i.e. observations) for use in parsing the config file. 

"""


# useful rules
#  include min and max rules max(IRS1) > max(Akt)
#  include option for numerical qualifier IRS1@t=45 > 2*Akt@t=45
#  use one hot encoding
# Encode clause1 and 2 individually


class _EncodingBase:
    TIME_SYMBOL_STR = '@t='

    _valid_functions = ['mean', 'all', 'min', 'max']
    _valid_mathematical_operators = ['+', '-', '/', '*', '**', ]
    _valid_operators = ['>', '=>', '<', '=<', '==', '!=']

    _function_pattern = [f'\A{i}' for i in _valid_functions]
    _function_pattern = '|'.join(_function_pattern)

    # _text_pattern = '\A[^@,][\w]*'
    _text_pattern = '\A[\w]+@'
    _digit_pattern = '\A\d+'
    _interval_pattern = '\A\(\d*[, ]+\d*\)'

    _operator_pattern = [f'\A{i}' for i in _valid_operators]
    _operator_pattern = '|'.join(_operator_pattern)

    _math_operator_pattern = '\A\+|\A-|\A/|\A\*|\A\*\*'

    _time_symbol_pattern = f'\At='

    _patterns = {
        _function_pattern: '_encode_functions',
        _text_pattern: '_encode_text',
        _time_symbol_pattern: '_encode_time_symbol',
        _digit_pattern: '_encode_digit',
        _interval_pattern: '_encode_interval',
        _operator_pattern: '_encode_operator',
        _math_operator_pattern: '_encode_math_operator',
    }

    TIME_SYMBOL_NUMBER = 1
    FUNC = 2
    TEXT = 3
    DIGIT = 4
    INTERAVL = 5
    OPERATOR = 6
    MATH_OPERATOR = 7

    vocab = {
        _function_pattern: FUNC,
        _text_pattern: TEXT,
        _digit_pattern: DIGIT,
        _interval_pattern: INTERAVL,
        _operator_pattern: OPERATOR,
        _math_operator_pattern: MATH_OPERATOR,
        _time_symbol_pattern: TIME_SYMBOL_NUMBER,
    }

    valid_combs = {
        ('point',): 1,
        ('interval',): 2,
        ('point', 'expression'): 3,
        ('fun', 'interval'): 4,
        ('interval', 'expression'): 5,
    }
    dupe_labels = [(k, k) for k in valid_combs.keys()]
    labels_decoder = dict(enumerate(dupe_labels + [i for i in combinations(valid_combs, 2)] ))
    labels_encoder = {v: k for k, v in labels_decoder.items()}


class Encoder(_EncodingBase):

    def __init__(self, clause):
        # for modifying
        self.clause = clause.strip()
        # for storing
        self.original_clause = deepcopy(clause.strip())

    def dispatch(self):
        l = []
        for pattern, method in self._patterns.items():
            match = re.findall(pattern, self.clause)
            if match:
                l.append(self.vocab[pattern])
                self.clause = re.sub(pattern, '', self.clause).strip()
                return l
        raise SyntaxError('No valid patterns have been found. ')

    def encode(self):
        seq = []
        done = False

        while not done:
            seq += self.dispatch()
            if self.clause == '':
                done = True
        return seq


class CreateTrainingData(_EncodingBase):

    def __init__(self, n_instances: int, seed=None, end_time=1000, fname=None) -> None:
        self.n_instances = n_instances
        self.seed = seed
        self.end_time = end_time
        self.fname = fname
        # self.data = self.label_data(self.create_data())

        if self.fname:
            self.data.to_csv(self.fname)

    def _sample_letters(self):
        if self.seed:
            np.random.seed(self.seed)
        word_length = np.random.choice(range(1, 11), )
        ascii = list(ascii_letters) + ['_'] * 10
        sample = np.random.choice(ascii, word_length)
        return ''.join(sample)

    def _sample_time(self):
        if self.seed:
            np.random.seed(self.seed)
        return np.random.choice(range(self.end_time))

    def point(self, text):
        time_sample = self._sample_time()
        return f'{text}@t={time_sample}'

    def interval(self, text):
        """
        Ensure second time is larger than first
        :param text:
        :return:
        """
        time1 = 1
        time2 = 0
        while time2 < time1:
            time1 = self._sample_time()
            time2 = self._sample_time()

        return f'{text}@t=({time1},{time2})'

    def fun(self, text):
        fun_sample = np.random.choice(self._valid_functions)
        return f'{fun_sample} {text}'

    def expression(self, text):
        operator_sample = np.random.choice(self._valid_mathematical_operators)
        constant_sample = np.random.choice(range(100))
        r = np.random.sample(1)
        return f'{constant_sample}{operator_sample}{text}' if r > 0.5 else f'{text}{operator_sample}{constant_sample}'

    def _create_clause(self):
        """

        :return:
        """
        text = self._sample_letters()
        label = np.random.choice(list(self.valid_combs.keys()))

        # now pipe text through labels starting at 0
        methods = [getattr(self, i) for i in label]
        for i in methods:
            text = i(text)
        return text, label

    @staticmethod
    def reduce_label(label):
        return reduce(lambda x, y: f'{x}{y}', label)

    def create_data(self):
        clauses, labels, encoding = [], [], []
        for i in range(self.n_instances):
            clause1, label1 = self._create_clause()
            clause2, label2 = self._create_clause()
            op = np.random.choice(self._valid_operators)
            clause = f'{clause1} {op} {clause2}'
            label = self.labels_encoder[(label1, label2)]
            clauses.append(clause)
            labels.append(label)
            e = Encoder(clause).encode()
            encoding.append(e)

        label = pd.DataFrame(labels, columns=['label'])
        clauses = pd.DataFrame(clauses, columns=['statement'])
        encoding = pd.DataFrame([encoding]).transpose()
        encoding.columns = ['encoding']
        df = pd.concat([clauses, encoding, label], axis=1)
        return df

    @staticmethod
    def label_data(data):
        clauses = data.iloc[:, 0]
        features = (data.iloc[:, 1:])
        # create vocab based on unique rows
        label_df = features.drop_duplicates().reset_index(drop=True)
        labels = []
        for i in range(features.shape[0]):
            f = features.iloc[i].values
            current_label = None
            j = 0
            while current_label is None:
                l = label_df.iloc[j].values
                if np.array_equal(f, l):
                    current_label = j
                j += 1
            labels.append(current_label)
        labels = pd.Series(labels, name='label')
        df = pd.concat([clauses, features, labels], axis=1)
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

    # need a df with point, interval etc as features. one hot encoding!

    # Create dataset
    CREATE_DATA = True

    # retrain model
    OVERWRITE_MODEL = False

    # load model from file
    LOAD_MODEL = False

    # train sequential model. Continues training if LOAD_MODEL is True
    TRAIN_MODEL = False

    if CREATE_DATA:
        N = 1000
        train = CreateTrainingData(int(0.8 * N), fname=TRAIN_DATA_FILE)
        test = CreateTrainingData(int(0.1 * N), fname=TEST_DATA_FILE)
        val = CreateTrainingData(int(0.1 * N), fname=VAL_DATA_FILE)

    train_data = pd.read_csv(TRAIN_DATA_FILE, index_col=0)
    test_data = pd.read_csv(TEST_DATA_FILE, index_col=0)
    val_data = pd.read_csv(VAL_DATA_FILE, index_col=0)

    train_labels = train_data['label']
    test_labels = test_data['label']
    val_labels = val_data['label']

    plt.figure()
    plt.hist(train_labels)
    plt.show()

    if TRAIN_MODEL:

        #
        if LOAD_MODEL:
            model = tf.keras.models.load_model(MODEL_PATH)
        else:
            dropout_param = 0.25
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, input_shape=(train_data.shape[1],), activation='tanh'),
                # tf.keras.layers.Embedding(6, 800),
                tf.keras.layers.Dropout(dropout_param),
                tf.keras.layers.Dense(32, activation='tanh'),
                tf.keras.layers.Dropout(dropout_param),
                tf.keras.layers.Dense(16, activation='relu'),
                tf.keras.layers.Dropout(dropout_param),
                # tf.keras.layers.Dense(16, activation='relu'),
                # tf.keras.layers.Dropout(dropout_param),
                tf.keras.layers.Dense(num_output, activation='softmax'),
            ])
            model.compile(
                optimizer='adam', loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
        if TRAIN_MODEL:
            # print(model.summary())
            # print(train_data)
            # print(train_data.shape)
            # print(train_labels)
            class PlotterCallback(tf.keras.callbacks.Callback):

                def on_epoch_end(self, epoch, logs=None):
                    from matplotlib.gridspec import GridSpec
                    grid = GridSpec(2, 2)
                    fig = plt.figure()
                    i = 0
                    for k, v in logs.items():
                        fig.add_subplot(grid[i])
                        plt.plot(v, label=k)
                        plt.title(k)
                        plt.legend()
                        sns.despine(fig=fig, top=True, right=True)
                        fname = os.path.join(DATA_DIR, '{}.png'.format(k))
                        plt.savefig(fname, dpi=300, bbox_inches='tight')
                        print('saved to "{}"'.format(fname))
                        i += 1


            tensorboard = tf.keras.callbacks.TensorBoard(log_dir="logs/{}".format(time()))
            early_stopping = tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                min_delta=0,
                patience=0,
                verbose=0, mode='auto'
            )

            history = model.fit(train_data, train_labels, batch_size=100, epochs=500,
                                validation_data=(val_data, val_labels),
                                callbacks=[tensorboard, early_stopping]
                                )

            for k, v in history.history.items():
                fig = plt.figure()
                plt.plot(v, label=k)
                plt.title(k)
                plt.legend()
                sns.despine(fig=fig, top=True, right=True)
                fname = os.path.join(DATA_DIR, '{}.png'.format(k))
                plt.savefig(fname, dpi=300, bbox_inches='tight')
                print('saved to "{}"'.format(fname))

            model.save(MODEL_PATH)

            results = model.evaluate(test_data, test_labels, batch_size=100)
            print(results)
            results = model.predict(test_data.iloc[:5])
            print(results)
            test_results = pd.DataFrame(results)
            # prediction = pd.concat([test_results.idxmax(1), test_labels[:5]], axis=1)
            # prediction.columns = ['predicted', 'actual']
            # print(prediction)
            print(test_results.idxmax(1))
            # print(test_labels)
