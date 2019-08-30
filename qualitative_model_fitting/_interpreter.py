import os, glob
import pandas as pd
import numpy as np
from lark import Tree, Token, Visitor, Transformer, v_args
import operator
from ._simulator import TimeSeries

class Interpreter:
    """
    Read a Lark tree into a set of classes.
    """

    def __init__(self, tree: Tree):
        """

        Args:
            tree:
        """
        self.tree = tree

    def _get_timeseries_blocks(self):
        return self.tree.find_data('timeseries_block')

    def _get_observation_block(self):
        return self.tree.find_data('observation_block')

    def interpret(self):
        ts_list = []
        for ts_block in self._get_timeseries_blocks():
            ts_list.append(self._timeseries_block(ts_block))

        obs = self.observation_block(self._get_observation_block())
        return ts_list, obs

    @staticmethod
    def _timeseries_block(block):
        """
        Intepret the time series block
        Args:
            block:

        Returns:

        """
        name = block.children[0]
        assert name.type == 'SYMBOL'
        name = name.value
        args = [i for i in block.find_data('ts_arg_list')]
        names = []
        amounts = []
        for arg_tree in args:
            for arg in arg_tree.children:
                for token in arg.children:
                    if token.type == 'SYMBOL':
                        names.append(str(token))
                    elif token.type == 'DIGIT' or token.type == 'FLOAT':
                        amounts.append(float(str(token.value)))
        ts_args = dict(zip(names, amounts))
        start = None
        stop = None
        step = None
        integration_settings = {'start': None, 'stop': None, 'step': None}
        for tok in block.children:
            if isinstance(tok, Tree):
                pass
            elif isinstance(tok, Token):
                if tok.type == 'START':
                    integration_settings['start'] = float(str(tok.value))
                elif tok.type == 'STOP':
                    integration_settings['stop'] = float(str(tok.value))
                elif tok.type == 'STEP':
                    integration_settings['step'] = float(str(tok.value))
        for k, v in integration_settings.items():
            if v == [] or v is None:
                raise ValueError

        return dict(name=name, conditions=ts_args, integration_settings=integration_settings)

    @staticmethod
    def observation_block(block):
        """
        interpret the observation block
        Args:
            block:

        Returns:

        """
        block = [i for i in block]
        if len(block) != 1:
            raise SyntaxError('There must be exactly 1'
                              ' observation block but found "{}"'.format(len(block)))
        block = block[0]
        statement_list = [i for i in block.find_data('statement')]
        new_statement_list = []
        for state in statement_list:
            s = _Observation(state)
            new_statement_list.append(s)
        return new_statement_list


class _Observation:

    def __init__(self, obs):  # clause1, op, clause2, name=None):
        self.obs = obs
        print('In obs')

    @property
    def name(self):
        # first element should be the name
        name = self.obs.children[0]
        assert name.type == 'OBS_NAME'
        return name.value

    @property
    def clause1(self):
        cl1 = self.obs.children[1]
        assert cl1.data == 'clause1'
        return _Clause(cl1)

    @property
    def operator(self):
        return _Operator(self.obs.children[2])

    @property
    def clause2(self):
        cl2 = self.obs.children[3]
        assert cl2.data == 'clause2'
        return _Clause(cl2)

    def __str__(self):
        return f'{self.name}: {self.clause1} {self.operator} {self.clause2}'

    def __repr__(self):
        return self.__str__()

    def reduce(self, ts_data, obs=None):
        print('obsversation reduce invoked')
        if obs is None:
            obs = self.obs

        elements = []
        for i in obs.children:
            # print(i)
            if isinstance(i, Tree):
                print('idata', i.data)
                if i.data == 'clause1':
                    elements.append(_Clause(i).reduce(ts_data))
                if i.data == 'clause2':
                    elements.append(_Clause(i).reduce(ts_data))
            elif isinstance(i, Token):
                elements.append(i)
        print('output of observation reduce')
        print(elements)
        return elements



class _Clause:

    def __init__(self, clause):  # model_component, condition, time, modifiers=None):
        self.clause = clause

        # self.model_entity, self.expression, self.modifier = self.reduce()

    def reduce(self, ts_data, clause=None):
        print('clause reduce invoked')
        if clause is None:
            clause = self.clause
        elements = []
        for i in clause.children:
            print('clause i is', i)
            if isinstance(i, Tree):
                if i.data == 'expression':
                    elements.append(_Expression(i).reduce(ts_data))
            elif isinstance(i, Token):
                if i.type == 'FUNC':
                    elements.append(getattr(np, i.value))
        print('Output of clause reduce')
        print(elements)
        return elements

    def __str__(self):
        return str(self.clause)
    #     if self.modifier:
    #         return f'{self.modifier.__name__} {str(self.model_entity)}'
    #     else:
    #         return f'{str(self.model_entity)}'
    #
    def __repr__(self):
        return self.__str__()


class _Expression:
    # type can be either 'numerical' for a pure expression
    #  or 'composite' for an expression where one of the operants
    #  is a model_entity

    def __init__(self, exprs):
        self.exprs = exprs
        # print(self.exprs)
        # print(self.exprs.pretty())

    def reduce(self, ts_data, expression=None):
        print('expression reduce invoked')
        reduced = None
        if expression is None:
            expression = self.exprs
        elements = []
        if not isinstance(expression, (Tree, Token)):
            return expression
        for i in expression.children:
            if isinstance(i, Tree):
                print('expression i is', i)
                if i.data == 'model_entity':
                    reduced = self.reduce(ts_data, _ModelEntity(i).reduce(ts_data))
        print('output of expression reduce')
        print(reduced)
        return reduced

    def compute(self):
        print('compute func')
        print(self.exprs)

    def __str__(self):
        return f'{self.exprs}'

    def __repr__(self):
        return self.__str__()



class _ModelEntity:
    time_type = None

    def __init__(self, model_entity):
        self.model_entity = model_entity

    @property
    def component_name(self):
        name = self.model_entity.children[0]
        assert name.type == 'SYMBOL'
        return name.value

    @property
    def condition(self):
        cond = self.model_entity.children[1]
        assert cond.type == 'CONDITION'
        return cond.value

    @property
    def time(self):
        time = self.model_entity.children[2]
        if time.type == 'POINT_TIME':
            self.time_type = 'POINT'
        elif time.type == 'INTERVAL_TIME':
            self.time_type = 'INTERVAL'
        else:
            raise SyntaxError
        return time.value

    def __str__(self):
        return f'{self.component_name}[{self.condition}]@t={self.time}'

    def __repr__(self):
        return self.__str__()

    def reduce(self, ts_data):
        print('model entity reduce invoked')
        time = eval(self.time)
        if isinstance(time, tuple):
            return ts_data[self.condition][self.component_name].loc[float(time[0]): float(time[1])]
        else:
            return ts_data[self.condition][self.component_name].loc[float(time)]

class _Operator:

    def __init__(self, op):
        self.op = op

    @property
    def operator(self):
        if self.op == '>':
            return operator.gt
        elif self.op == '<':
            return operator.lt
        elif self.op == '>=':
            return operator.le
        elif self.op == '<=':
            return operator.le
        elif self.op == '!=':
            return operator.ne
        elif self.op == '==':
            return operator.eq
        else:
            raise SyntaxError(self.op)

    def __str__(self):
        return self.op

    def __repr__(self):
        return self.__str__()
