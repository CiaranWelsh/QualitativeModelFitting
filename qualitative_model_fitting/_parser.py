import os, glob, re
from copy import deepcopy
from itertools import combinations

import pandas as pd
import numpy as np

import parser_training
import qualitative_model_fitting
from qualitative_model_fitting import _simulator


class _Parser:

    def __init__(self, statement: (str, list)) -> None:
        self._statement = statement
        if isinstance(self._statement, str):
            self._statement = [self._statement]

        self.statements = self._to_df()

    def _encode_statements(self):
        encoded = []
        matches = []
        for i in self._statement:
            e, m = Encoder(i).encode()
            encoded.append(e)
            matches.append(m)
        return encoded, matches

    def _to_df(self):
        s = pd.DataFrame(self._statement)
        s.columns = ['statement']
        e, m = self._encode_statements()
        e = pd.DataFrame([e]).transpose()
        e.columns = ['encoded']
        m = pd.DataFrame([m]).transpose()
        m.columns = ['matches']
        return pd.concat([s, e, m], axis=1)


class Encoder:
    TIME_SYMBOL_STR = '@t='

    _valid_functions = ['mean', 'all', 'min', 'max', 'any', 'sum']
    _valid_mathematical_operators = ['+', '-', '/', '*', '**', ]
    _valid_operators = ['>', '>=', '<', '<=', '==', '!=']

    _function_pattern = [f'\A{i}' for i in _valid_functions]
    _function_pattern = '|'.join(_function_pattern)

    _text_pattern = '\A(?!\d+)(\w+)(?=[@+/*-]*)'
    _digit_pattern = '\A(\d+)'
    _interval_pattern = '\A(\(\d*[, ]+\d*\))'

    # use look aheads and look behinds here
    _operator_pattern = '\A([<=>!]{1,2})'

    _math_operator_pattern = '\A(\+)|\A(-)|\A(/)|\A(\*{1,2})'

    _time_symbol_pattern = f'\A(@t=)'

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
    INTERVAL = 5
    OPERATOR = 6
    MATH_OPERATOR = 7

    labels = {
        'time_symbol': 1,
        'func': 2,
        'text': 3,
        'digit': 4,
        'interval': 5,
        'mathematical_operator': 6,
        'math_operator': 7,
    }

    vocab = {
        _function_pattern: FUNC,
        _text_pattern: TEXT,
        _digit_pattern: DIGIT,
        _interval_pattern: INTERVAL,
        _operator_pattern: OPERATOR,
        _math_operator_pattern: MATH_OPERATOR,
        _time_symbol_pattern: TIME_SYMBOL_NUMBER,
    }

    valid_combs = {
        ('point',): 1,
        ('interval',): 2,
        ('point', 'expression'): 3,
        ('expression', 'point'): 3,
        ('fun', 'interval'): 4,
        ('expression', 'interval'): 5,
        ('interval', 'expression'): 5,
    }
    dupe_labels = [(k, k) for k in valid_combs.keys()]
    labels_decoder = dict(enumerate(dupe_labels + [i for i in combinations(valid_combs, 2)]))
    labels_encoder = {v: k for k, v in labels_decoder.items()}

    def __init__(self, clause):
        # for modifying
        self.clause = clause.strip()
        # for storing
        self.original_clause = deepcopy(clause.strip())

    def _encode_part(self):
        # todo rename dispatch. Didn't use this as a dispatcher in the end
        indicators = []
        matches = []
        for pattern, method in self._patterns.items():
            if qualitative_model_fitting.VERBOSE:
                print('clause is', self.clause)
                print('pattern is:', pattern)
                print('method is:', method)

            match = re.findall(pattern, self.clause)
            if qualitative_model_fitting.VERBOSE:
                print('match is:', match)
                print('\n')

            if match:
                indicators.append(self.vocab[pattern])
                matches += match
                self.clause = re.sub(pattern, '', self.clause).strip()
                return indicators, matches

        raise SyntaxError('No valid patterns have been found for clause "{}"'.format(self.clause))

    def encode(self):
        match_seq = []
        ind_seq = []

        done = False
        while not done:
            ind, match = self._encode_part()
            if not match:
                raise ValueError('Have not been able to match anything. Check your inputs.')

            # Deal with the tuple case for mathematical operators
            if isinstance(match[0], tuple):
                match = [i for i in list(match[0]) if i != '']
            ind_seq += ind
            match_seq += match
            if self.clause == '':
                done = True
        return ind_seq, match_seq
