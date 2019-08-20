import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from time import time
from string import ascii_letters
import tensorflow as tf
from functools import reduce

# todo think about multi-label classification
from qualitative_model_fitting import _Encoder
from qualitative_model_fitting._parser import _EncodingBase

"""
Create a keras model for classifying rules (i.e. observations) for use in parsing the config file. 

"""


# useful rules
#  include min and max rules max(IRS1) > max(Akt)
#  include option for numerical qualifier IRS1@t=45 > 2*Akt@t=45
#  use one hot encoding
# Encode clause1 and 2 individually


class CreateTrainingData(_EncodingBase):

    def __init__(self, n_instances: int, seed=None, end_time=1000, fname=None) -> None:
        self.n_instances = n_instances
        self.seed = seed
        self.end_time = end_time
        self.fname = fname
        self.data = self.create_data()

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
        Ensure second interval_time is larger than first
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
            # label = self.labels_encoder[(label1, label2)]
            clauses.append(clause)
            # labels.append(label)
            e = _Encoder(clause).encode()
            encoding.append(e)

        # label = pd.DataFrame(labels, columns=['label'])
        clauses = pd.DataFrame(clauses, columns=['statement'])
        encoding = pd.DataFrame([encoding]).transpose()
        encoding.columns = ['encoding']
        df = pd.concat([clauses, encoding], axis=1)
        return df

    @staticmethod
    def label_data(data):
        clauses = data.iloc[:, 0]
        print(clauses)
        # features = (data.iloc[:, 1:])
        # # create vocab based on unique rows
        # label_df = features.drop_duplicates().reset_index(drop=True)
        # labels = []
        # for i in range(features.shape[0]):
        #     f = features.iloc[i].values
        #     current_label = None
        #     j = 0
        #     while current_label is None:
        #         l = label_df.iloc[j].values
        #         if np.array_equal(f, l):
        #             current_label = j
        #         j += 1
        #     labels.append(current_label)
        # labels = pd.Series(labels, name='label')
        # df = pd.concat([clauses, features, labels], axis=1)
        # return df


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

    print(train_data)

    train_X = train_data['encoding']
    # train_y = train_data['label']
    test_X = test_data['encoding']
    # test_y = test_data['label']
    val_X = val_data['encoding']
    # val_y = val_data['label']

    # output layer
    # num_output = len(train_data['label'].unique())
    print(train_X)

    # plt.figure()
    # plt.hist(train_labels)
    # plt.show()

    if TRAIN_MODEL:

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
