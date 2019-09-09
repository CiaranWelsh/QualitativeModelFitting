import os, glob
import pandas as pd
import numpy as np
from functools import reduce
from lark import Tree, Token, Visitor, Transformer, v_args
import operator
from ._simulator import TimeSeries

import logging

LOG = logging.getLogger(__name__)



class _Base:

    def __init__(self):
        pass

    @staticmethod
    def reduce_model_entity(entity, ts_data, function_modifier=None):
        token = _ModelEntity(entity).reduce(ts_data)
        LOG.debug('Clause.data is a model entity, we can reduce here and return {}'.format(token))
        if isinstance(token, (float, int)):
            token = Token('NUMBER', token)
            LOG.debug('token is {}'.format(token))
            return token
        elif isinstance(token, Token):
            return token
        elif isinstance(token, pd.Series):
            return token
            # if function_modifier is None:
            #     raise SyntaxError('specify a function')
            # if not callable(function_modifier):
            #     raise ValueError
            # token = function_modifier(token)
            # token = Token('NUMBER', token)
            # return token

        else:
            raise ValueError(token)

    @staticmethod
    def reduce_expression(exprs, ts_data):
        token = _Expression(exprs).reduce(ts_data, exprs)
        LOG.debug('clause is an expression or term. resulting token is: {}, {}'.format(token, type(token)))
        return token

    @staticmethod
    def reduce_if_all_children_are_tokens(tree, ts_data):
        LOG.debug('clause is {}, {}'.format(tree.data, tree.children))
        LOG.debug('All clause children are tokens. Reducing and returning')
        reduced = reduce(lambda x, y: f'{str(x)} {str(y)}', tree.children)
        LOG.debug('reduced is: {}'.format(reduced))
        LOG.debug('reduced type is: {}'.format(type(reduced)))
        if isinstance(reduced, str):
            reduced = eval(reduced)

        if isinstance(reduced, (float, int)):
            token = Token('NUMBER', reduced)
            LOG.debug(f'returning reduced token {token}')
            return token
        elif isinstance(reduced, Token):
            return reduced

        else:
            raise ValueError(reduced)

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
        LOG.debug('obsversation reduce invoked')
        if obs is None:
            obs = self.obs

        cl1 = None
        cl2 = None
        operator = None
        for i in obs.children:
            # LOG.debug(i)
            if isinstance(i, Tree):
                if i.data == 'clause1':
                    cl1 = _Clause(i).reduce(ts_data)
                if i.data == 'clause2':
                    cl2 = _Clause(i).reduce(ts_data)
            elif isinstance(i, Token):
                if i.type == 'OPERATOR':
                    operator = i
                elif i.type == 'OBS_NAME':
                    obs_name = i
                else:
                    raise SyntaxError(f'Token {i.type} is invalid')
        LOG.debug('output of observation reduce')
        LOG.debug(f'full observation comparison is: "{cl1} {str(operator)} {cl2}"')
        return {'obs_name': obs_name,
                'evaluation': eval(f'{cl1} {str(operator)} {cl2}'),
                'comparison': f'{cl1} {str(operator)} {cl2}'}


class _Clause(_Base):

    def __init__(self, clause):  # model_component, condition, time, modifiers=None):
        self.clause = clause

    def reduce(self, ts_data, clause=None):
        LOG.debug('clause reduce invoked')
        if clause is None:
            clause = self.clause

        LOG.debug('clause is {}'.format(clause))

        if not isinstance(clause, (Tree, Token)):
            raise TypeError('need Token or Tree but found "{}" of type "{}"'.format(clause, type(clause)))

        if isinstance(clause, Tree):
            LOG.debug(f'clause is a tree')
            if clause.data == 'model_entity':
                return self.reduce_model_entity(clause, ts_data)

            elif clause.data in ['expression', 'term']:
                return self.reduce_expression(clause, ts_data)

            elif all([isinstance(i, Token) for i in clause.children]):
                return self.reduce_if_all_children_are_tokens(clause, ts_data)

            elif clause.data in ['clause1', 'clause2']:
                # recursively call self.reduce on each of the clause children
                reduced_list = [self.reduce(ts_data, i) for i in clause.children]
                LOG.debug('reduced list is {}'.format(reduced_list))
                if len(reduced_list) == 0:
                    raise ValueError

                elif len(reduced_list) == 1:
                    if isinstance(reduced_list[0], (float, int)):
                        return self.reduce(ts_data, Token('NUMBER', reduced_list[0]))
                    elif isinstance(reduced_list[0], Token):
                        return reduced_list[0]
                    else:
                        raise ValueError

                elif len(reduced_list) == 2:
                    LOG.debug('reduce_list is len 2: {}'.format(reduced_list))
                    if reduced_list[0].type == 'FUNC':
                        if not hasattr(np, str(reduced_list[0])):
                            raise SyntaxError(f'{reduced_list[0]} is not a valid function.')
                        func = getattr(np, str(reduced_list[0]))
                        token = func(reduced_list[1])
                        if isinstance(token, (float, int)):
                            token = Token('NUMBER', token)
                            return token
                        # elif isinstance(token, bool):
                        #     return token
                        else:
                            raise ValueError(token)
                    else:
                        raise ValueError

                elif len(reduced_list) > 2:
                    return self.reduce(ts_data, Tree('expression', reduced_list))

                else:
                    raise ValueError

            else:
                raise ValueError(clause.data)
        # and deal with the case where clause is a token
        elif isinstance(clause, Token):
            LOG.debug('our clause is a token: {}, type: {}'.format(clause, type(clause)))
            return clause
        else:
            raise ValueError



    def __str__(self):
        return str(self.clause)

    def __repr__(self):
        return self.__str__()


class _Expression(_Base):
    # type can be either 'numerical' for a pure expression
    #  or 'composite' for an expression where one of the operants
    #  is a model_entity

    def __init__(self, exprs):
        self.exprs = exprs

    @staticmethod
    def _reduce_numerical_expression(*args):
        from functools import reduce
        string = reduce(lambda x, y: f'{str(x)} {str(y)}', args)
        return eval(string)

    def reduce(self, ts_data, expression=None):
        LOG.debug('expression reduce invoked')
        # reduced = None
        if expression is None:
            expression = self.exprs

        if not isinstance(expression, Tree):
            raise TypeError

        if expression.data == 'model_entity':
            return self.reduce_model_entity(expression, ts_data)

        if all([isinstance(i, Token) for i in expression.children]):
            return self.reduce_if_all_children_are_tokens(expression, ts_data)
        else:
            LOG.debug('expression.childre are not all tokens: {}'.format(expression))
            l = []
            for i in expression.children:
                if isinstance(i, Tree):
                    l.append(self.reduce(ts_data, i))
                elif isinstance(i, Token):
                    l.append(i)
                else:
                    raise ValueError(i)
            LOG.debug('list is {}'.format(l))
            return self.reduce(ts_data, Tree('expression', l))

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
        LOG.debug('model entity reduce invoked')
        time = eval(self.time)
        if isinstance(time, tuple):
            output = ts_data[self.condition][self.component_name].loc[float(time[0]): float(time[1])]
        else:
            output = ts_data[self.condition][self.component_name].loc[float(time)]
        LOG.debug('model entity reduce output is: ')
        LOG.debug(output)
        return output


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
