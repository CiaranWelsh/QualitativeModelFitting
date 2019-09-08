import os, glob
import pandas as pd
import numpy as np
from lark import Tree, Token, Visitor, Transformer, v_args
import operator
from ._simulator import TimeSeries

import logging

LOG = logging.getLogger(__name__)


# LOG.setLevel(logging.DEBUG)
# print(LOG)


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


class _Clause:

    def __init__(self, clause):  # model_component, condition, time, modifiers=None):
        self.clause = clause

        # self.model_entity, self.expression, self.modifier = self.reduce()

    def reduce(self, ts_data, clause=None):
        LOG.debug('clause reduce invoked')
        if clause is None:
            clause = self.clause

        elements = []
        for i in clause.children:
            if isinstance(i, Tree):
                if i.data == 'expression':
                    exp = _Expression(i).reduce(ts_data)
                    elements.append(exp)
            elif isinstance(i, Token):
                if i.type == 'FUNC':
                    elements.append(getattr(np, i.value))
        LOG.debug('Output of clause reduce')
        LOG.debug(elements)
        if len(elements) == 1:
            if isinstance(elements[0], (float, int)):
                token = elements[0]
            elif isinstance(elements[0], Token):
                token = eval(str(elements[0]))
            else:
                raise ValueError
            return token
        # if we have >1 item in elements we need to reduce the clause further
        elif len(elements) == 2:
            # Deal with situation where we have a series and a function modifier (i.e. mean A[CondY]@t=(0, 5))
            if callable(elements[0]):
                # can only apply a modifier on a collection obj such as series
                if not isinstance(elements[1], pd.Series):
                    raise SyntaxError(f'Cannot apply function modifier to a single entity. You have '
                                      f'tried to apply the {elements[0]} function to '
                                      f'{elements[1]}')
                else:
                    return elements[0](elements[1])
        else:
            raise SyntaxError(clause)

    def __str__(self):
        return str(self.clause)

    def __repr__(self):
        return self.__str__()


class _Expression:
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

    def _process_expression(self, ts_data, expression):
        LOG.debug('_process_expression invoked')
        if all([isinstance(i, Token) for i in expression.children]):
            LOG.debug(f'all children are tokens. Reducing. {expression.children}')
            return self._reduce_numerical_expression(*expression.children)
        else:
            LOG.debug(f'all children are not tokens. {expression.children}')
            new_children = []
            for i, element in enumerate(expression.children):
                LOG.debug(element)
                if isinstance(element, Tree):
                    if element.data == 'expression':
                        res = self._process_expression(ts_data, element)
                        LOG.debug(f'result of process expresssion is {res}')
                        new_children.append(res)
                        LOG.debug(f'new children list is {new_children}')

                    else:
                        raise ValueError(i)
                elif isinstance(i, Token):
                    new_children.append(i)
            tree = Tree('expression', new_children)
            LOG.debug(f'tree with new exprs {tree}')
            return self._process_expression(ts_data, tree)
            # return self.reduce(ts_data, expression.children[0])

    def reduce(self, ts_data, expression=None):
        LOG.debug('expression reduce invoked')
        # reduced = None
        if expression is None:
            expression = self.exprs
        LOG.debug('expression is {}'.format(expression.pretty()))
        if isinstance(expression, Tree):
            if expression.data == 'expression':
                return self._process_expression(ts_data, expression)
            elif expression.data == 'model_entity':
                reduced_model_entity = _ModelEntity(expression).reduce(ts_data)
                return self.reduce(ts_data, reduced_model_entity)
            else:
                raise NotImplementedError
        elif isinstance(expression, Token):
            if expression.type == 'NUMBER':
                return expression
        elif isinstance(expression, (float, int, pd.Series)):
            LOG.debug('final expression ', expression)
            return expression

    def reduce2(self, ts_data, expression=None):
        LOG.debug('expression reduce invoked')
        # reduced = None
        if expression is None:
            expression = self.exprs
        if expression.children == []:
            raise ValueError('expression.children is an empty list')
        # elements = []
        LOG.debug('expression is: ', expression)
        if not isinstance(expression, (Tree, Token)):
            raise ValueError
        try:
            str_exp
        except UnboundLocalError:
            str_exp = ''
        LOG.debug('expression and children (second)', expression, expression.children)
        for i, ele in enumerate(expression.children):
            LOG.debug(type(ele), ele)
            if isinstance(ele, Tree):
                LOG.debug('expression element i is a ', ele.data, type(ele), ele)
                if ele.data == 'model_entity':
                    # reduce the model entity and coerce the output (which should be float) into a NUMBER Token
                    model_entity_reduced = Token('NUMBER', _ModelEntity(ele).reduce(ts_data))
                    LOG.debug('model entity reduced is: ', model_entity_reduced, 'type', type(model_entity_reduced))
                    LOG.debug('exp children before del', expression.children)
                    from copy import deepcopy
                    children = deepcopy(expression.children)
                    del children[i]
                    LOG.debug('exp children after del', children)
                    # reconstruct a tree and feed back into reduce with a simpler tree
                    LOG.debug('list concat', [model_entity_reduced] + children)
                    tree = Tree(expression.data, children=[model_entity_reduced] + children)
                    LOG.debug('Entering model entity recursion')
                    return self.reduce(ts_data, tree)
                # do not delete this commented out section. We still may need it for recursive expressions
                elif ele.data == 'expression':
                    LOG.debug('doing an expression')
                #     # str_exp = ''
                #     LOG.debug('we have an expression: ', ele.data)
                #     for ele2 in ele.children:
                #         if isinstance(ele2, Tree):
                #             raise ValueError('Recieved a Tree but was expecting list of Tokens')
                #         elif isinstance(ele2, Token):
                #             str_exp += str(ele2)

                else:
                    raise SyntaxError
            elif isinstance(ele, Token):
                LOG.debug('expression element i is a token ', ele.type, ele, str(ele))
                str_exp += str(ele)
                LOG.debug(str_exp)
        # LOG.debug(str_exp)
        # if str_exp == '':
        #     raise ValueError('str_exp is empty')
        LOG.debug('expression is (second)', expression)
        LOG.debug('expression reduced str_Exp: ', str_exp, type(str_exp))
        # return str_exp
        LOG.debug('eval of str_exp:', eval(str_exp))
        return eval(str_exp)

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
