import numpy as np
import pandas as pd
import os, glob, re
import matplotlib.pyplot as plt
import seaborn as sns

from time import time
from io import StringIO
from string import ascii_letters
from typing import Optional
import tensorflow as tf
from functools import reduce

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


class _Base:
    operators = ['>', '<', '>=', '<=', '=', '!=']

    label_encodings = {
        'point': '11',
        'range': '12',
        'fun': '13',
        'const': '14',
        'expression': '15',
    }
    label_decodings = {v: k for k, v in label_encodings.items()}
    operator_offset = len(label_encodings) + int(label_encodings['point'])
    operator_encodings = dict(
        zip(operators, ['{:02d}'.format(i) for i in range(operator_offset, len(operators) + operator_offset)])
    )
    operator_decodings = {k: v for v, k in operator_encodings.items()}

    valid_functions = ['max', 'min', 'mean', 'all']
    numerical_operators = ['*', '/', '+', '-', '**']

    valid_combs = [
        (label_encodings['point'],),
        (label_encodings['range'],),
        (label_encodings['const'],),
        (label_encodings['point'], label_encodings['expression']),
        (label_encodings['range'], label_encodings['fun']),
        (label_encodings['range'], label_encodings['expression']),
    ]

    nchar = len(label_encodings['point'])


class CreateTrainingData(_Base):

    def __init__(self, n_instances: int, seed=None, end_time=1000, fname=None) -> None:
        self.n_instances = n_instances
        self.seed = seed
        self.end_time = end_time
        self.fname = fname
        self.data = self.label_data(self.create_data())

        if self.fname:
            self.data.to_csv(self.fname)

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

    def point(self, text):
        time_sample = self.sample_time()
        return f'{text}@t={time_sample}'

    def range(self, text):
        """
        Ensure second time is larger than first
        :param text:
        :return:
        """
        time1 = 1
        time2 = 0
        while time2 < time1:
            time1 = self.sample_time()
            time2 = self.sample_time()

        return f'{text}@t=({time1},{time2})'

    def fun(self, text):
        fun_sample = np.random.choice(self.valid_functions)
        return f'{fun_sample}({text})'

    def const(self, text):
        num = np.random.choice(np.linspace(0.1, 10))
        return f'{round(num, 2)}'

    def expression(self, text):
        operator_sample = np.random.choice(self.numerical_operators)
        constant_sample = self.const(text)
        r = np.random.sample(1)
        return f'{constant_sample}{operator_sample}{text}' if r > 0.5 else f'{text}{operator_sample}{constant_sample}'

    def create_clause(self):
        """

        :return:
        """
        text = self._sample_letters()
        idx = list(range(len(self.valid_combs)))
        idx = np.random.choice(idx)
        feature_ids = self.valid_combs[idx]
        feature_names = [self.label_decodings[i] for i in feature_ids]
        one_hot_features = {i: 0 for i in self.label_encodings.keys()}
        update_features = {i: 1 for i in feature_names}
        one_hot_features.update(update_features)

        # now pipe text through labels starting at 0
        methods = [getattr(self, i) for i in feature_names]
        for i in methods:
            text = i(text)
        one_hot_features = pd.Series(one_hot_features)
        return text, one_hot_features

    def reduce_label(self, label):
        return reduce(lambda x, y: f'{x}{y}', label)

    def create_data(self):
        clauses, features, labels = [], [], []
        for i in range(self.n_instances):
            clause, f = self.create_clause()
            clauses.append(clause)
            features.append(f)

        clauses = pd.DataFrame(clauses, columns=['clause'])
        features = pd.DataFrame(features)
        df = pd.concat([clauses, features], axis=1)
        # print(df)
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


class Decoder(_Base):

    def __init__(self):
        pass

    def decode(self, label):
        label = str(label)
        begin = 0
        end = self.nchar
        size = int(len(label) / self.nchar)
        l = []
        for i in range(size):
            l.append(label[begin: end])
            begin = end
            end += self.nchar
        # find the operator first
        operator_idx = None
        for i in range(len(l)):
            try:
                operator = self.operator_decodings[l[i]]
                operator_idx = i
            except KeyError:
                continue
        clause1 = l[:operator_idx]
        clause2 = l[operator_idx + 1:]
        clause1 = [self.label_decodings[i] for i in clause1]
        clause2 = [self.label_decodings[i] for i in clause2]
        return clause1, operator, clause2


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

    # need a df with point, range etc as features. one hot encoding!

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

    # tok = tf.keras.preprocessing.text.Tokenizer(6, filters=ascii_letters+',.')
    # print(train_data['clause'].head())
    # tok.fit_on_texts(train_data['clause'])
    # print(tok.word_counts)
    # print(tok.texts_to_sequences(train_data['clause']))

    train_labels = train_data['label']
    test_labels = test_data['label']
    val_labels = val_data['label']
    #
    num_output = len(train_labels.unique())
    print(train_labels)
    print(train_labels.unique())
    print('number of labels', num_output)

    print(train_data[['clause']])

    # train_labels = tf.keras.utils.to_categorical(train_labels)
    # test_labels = tf.keras.utils.to_categorical(test_labels)
    # val_labels = tf.keras.utils.to_categorical(val_labels)
    # print(x)

    # for i in [train_data, test_data, val_data]:
    #     i.drop('label', axis=1)
        # i = i[['point', 'range']]

    # plt.figure()
    # plt.hist(train_labels)
    # plt.show()

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
