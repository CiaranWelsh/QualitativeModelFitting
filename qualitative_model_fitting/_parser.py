import os, glob, re
import pandas as pd
import numpy as np
import tensorflow as tf

from qualitative_model_fitting import _simulator
from parser_training._parser_training import _Base, EncoderOld, DecoderOld

# registery for rules classes
REGISTERED_MUTEXCL_RULES = set()
REGISTERED_COMB_RULES = set()


class Parser:

    model_file = os.path.join(os.path.dirname(__file__), 'nn_model.h5')
    if not os.path.isfile(model_file):
        raise FileNotFoundError(model_file)

    model = tf.keras.models.load_model(model_file)

    def __init__(self, rules: str) -> None:
        self.rules = rules
        if isinstance(self.rules, str):
            self.rules = [self.rules]

    def classify(self):
        labels = []
        for rule in self.rules:
            enc = EncoderOld()
            dec = DecoderOld()
            encoded = enc.preprocess(rule)
            X = encoded.iloc[0, 1:].values
            X = X.reshape(1, -1)
            y = self.model.predict(X)
            y = pd.DataFrame(y)
            encoded_label = y.idxmax(1)[0]
            label = dec.decode(encoded_label)
            labels.append(label)
        return labels

