import operator
from collections import OrderedDict
from functools import reduce

import numpy as np
import pandas as pd
from lark import Lark, Transformer, v_args, Visitor, Token, Tree

from ._simulator import TimeSeries

# todo implement combinations modifier
import logging

LOG = logging.getLogger(__name__)


class Parser:
    grammar = """
    start                  : block+
    ?block                  : timeseries_block  
                            | steadystate_block
                            | observation_block 
    timeseries_block        : "timeseries" NAME "{" ts_arg_list "}" START "," STOP "," STEP
    steadystate_block       : "steadystate" NAME "{" ts_arg_list "}" 
    ?ts_arg_list            : (ts_arg [","])*
    ?ts_arg                 : NAME "=" FLOAT 
                            | NAME "=" DIGIT+
                            
    
    observation_block       : "observation" statement+
    ?statement              : comparison_statement | behavioural_statement
    comparison_statement    : OBS_NAME ":" clause1 OPERATOR clause2
    behavioural_statement   : OBS_NAME ":" qual_exp 
    clause1                 : [function] expression
    clause2                 : [function] expression
    
    ?expression             : term ((ADD|SUB) term)*
    ?term                   : factor ((MUL
                                      |DIV 
                                      |MOD
                                      |FLOOR) factor)*
    ?factor                 : ("+"|"-") factor 
                            | atom
                            | power
    ?power                  : atom "**" factor
    ?atom                   : NUMBER 
                            | NAME
                            | model_entity
    
    ?model_entity           : NAME "[" CONDITION "]" [_TIME_SYMBOL (POINT_TIME| INTERVAL_TIME)] 
    ?function               : FUNC
    ?qual_exp                : SHAPE [DIRECTION] model_entity
    
    SHAPE                   : "hyperbolic"
                            | "transient"
                            | "sigmoidal"
                            | "oscillation"
    DIRECTION               : "up" 
                            | "down"
    
    OPERATOR                : ">"
                            | "<" 
                            | "==" 
                            | "!="
                            | "<="
                            | ">="
    FUNC                    : "mean"|"all"|"any"|"min"|"max"
    _TIME_SYMBOL            : "@t=" 
    POINT_TIME              :  DIGIT+
    INTERVAL_TIME           : "(" DIGIT+ [WS]* "," [WS]* DIGIT + ")"
    OBS_NAME                : NAME
    CONDITION               : NAME
    NAME                    : /(?!\d+)[A-Za-z0-9]+/
    START                   : DIGIT+
    STOP                    : DIGIT+
    STEP                    : DIGIT+
    POW                     : "**"
    MUL                     : "*"
    DIV                     : "/"
    ADD                     : "+"
    SUB                     : "-"
    MOD                     : "%"
    FLOOR                   : "//"
    NUMERICAL_OPERATOR      : "+"
                            | "-"
                            | "*"
                            | "/"
                            | "**"
                            | "//"
                            | "%"
    COMMENT                 : /\/\/.*/
    %import common.DIGIT
    %import common.NUMBER
    %import common.FLOAT
    %import common.WORD
    %import common.LETTER
    %import common.WS
    %ignore WS
    %ignore COMMENT
    """

    def __init__(self, model_string, observation_string):
        self.observation_string = observation_string
        self.model_string = model_string
        self.lark = Lark(self.grammar)
        self.tree = self.parse()
        self.ts_blocks, self.observation_block = self.objectify()

    def parse(self, string=None):
        if string is None:
            string = self.observation_string
        return self.lark.parse(string)

    def pretty(self, string=None):
        if string is None:
            string = self.observation_string
        return self.lark.parse(string).pretty()

    def objectify(self):
        ts_dct = {}
        for ts_block in self.tree.find_data('timeseries_block'):
            name = str(ts_block.children[0])
            ts_dct[name] = _TimeSeriesBlock(self.model_string, ts_block)

        ss_list = []
        for ss_block in self.tree.find_data('steady_state_block'):
            LOG.warning('steady state functionality is currently a placeholder. '
                        'Not yet implemented')

        observation_block = ObservationBlock(ts_dct)
        observations = [i for i in self.tree.find_data('observation_block')][0]
        for i in observations.children:
            if i.data == 'comparison_statement':
                observation_block.append(_ComparisonStatement(i, ts_dct))
            elif i.data == 'qualitative_statement':
                pass
            else:
                raise ValueError

        return ts_dct, observation_block


class _TimeSeriesBlock:
    start = None
    stop = None
    step = None
    name = None

    def __init__(self, model_string, ts_block):
        self.model_string = model_string
        self.ts_block = ts_block
        self.name, self.start, self.stop, self.step = self._get_ts_parameters()

        self.ts_arg_list = _TimeSeriesArgumentList()
        for i in self.ts_block.iter_subtrees():
            if isinstance(i, Tree):
                if i.data == 'ts_arg':
                    self.ts_arg_list.append(_TimeSeriesArgument(i))

            else:
                raise ValueError

    def _get_ts_parameters(self):
        start = None
        stop = None
        step = None
        name = None
        for i in self.ts_block.children:
            if isinstance(i, Tree):
                pass

            elif isinstance(i, Token):
                if i.type == 'START':
                    start = float(str(i))
                elif i.type == 'STOP':
                    stop = float(str(i))
                elif i.type == 'STEP':
                    step = int(str(i))
                elif i.type == 'NAME':
                    name = str(i)
            else:
                raise ValueError
        for i in [name, start, stop, step]:
            if i is None:
                raise SyntaxError(i)
        return name, start, stop, step

    def simulate(self):
        data = TimeSeries(self.model_string, self.ts_arg_list.to_dict(),
                          self.start, self.stop, self.step).simulate()
        return data

    def __str__(self):
        if len(self.ts_arg_list) == 1:
            ts_arg_list = self.ts_arg_list.children[0]
        else:
            ts_arg_list = reduce(lambda x, y: f'{x}, {y}', self.ts_arg_list)
        return f"{self.__class__.__name__}(timeseries {self.name} {{ {ts_arg_list} }} {self.start}, {self.stop}, {self.step})"

    def __repr__(self):
        return self.__str__()


class _TimeSeriesArgumentList(list):

    def __init__(self, *args):
        self.args = args
        self._check_all_elements_are_ts_arg()

    def _check_all_elements_are_ts_arg(self):
        for i in self:
            if i.data != 'ts_arg':
                raise ValueError('Was expecting a TimeSeriesArgument but got "{}"'.format(type(i)))

    def to_dict(self):
        dct = {}
        for i in self:
            dct[str(i.name)] = float(str(i.amount))
        return dct


class _TimeSeriesArgument:

    def __init__(self, ts_arg):
        self.ts_arg = ts_arg

        if ts_arg.data != 'ts_arg':
            raise ValueError

        if len(ts_arg.children) != 2:
            raise ValueError('was expecting two arguments but got "{}"'.format(len(ts_arg.children)))

    @property
    def name(self):
        return self.ts_arg.children[0]

    @property
    def amount(self):
        return self.ts_arg.children[1]

    def __str__(self):
        return f'{self.name}={self.amount}'

    def __repr__(self):
        return self.__str__()


class ObservationBlock(list):

    def __init__(self, ts_list, *args):
        self.ts_list = ts_list
        self.args = args
        super(ObservationBlock, self).__init__(*args)

        for i in self.args:
            if not isinstance(i, (_ComparisonStatement)):
                raise TypeError(i)


class _ComparisonStatement:
    name = None
    operator = None
    clause1 = None
    clause2 = None

    def __init__(self, statement, ts_list):
        self.statement = statement
        self.ts_list = ts_list

        for i in self.statement.children:
            if isinstance(i, Token):
                if i.type == 'OBS_NAME':
                    self.name = str(i)
                elif i.type == 'OPERATOR':
                    self.operator = str(i)
            elif isinstance(i, Tree):
                if i.data == 'clause1':
                    self.clause1 = _Clause(i, self.ts_list)
                elif i.data == 'clause2':
                    self.clause2 = _Clause(i, self.ts_list)

    def __str__(self):
        return f'{self.name}: {self.clause1} {self.operator} {self.clause2}'

    def __repr__(self):
        return self.__str__()


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


class _Observation:
    # comparison or
    type = 'comparison'

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
        assert cl1.type == 'clause1'
        return _Clause(cl1)

    @property
    def operator(self):
        return _Operator(self.obs.children[2])

    @property
    def clause2(self):
        cl2 = self.obs.children[3]
        assert cl2.type == 'clause2'
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

    def __init__(self, clause, ts_list):  # model_component, condition, time, modifiers=None):
        self.clause = clause
        self.ts_list = ts_list
        self.clause_elements = self._objectify_clause_elements()

    def _objectify_clause_elements(self):
        clause_elements = list()
        for i in self.clause.children:
            if isinstance(i, Token):
                clause_elements.append(i)
            elif isinstance(i, Tree):
                if i.data == 'model_entity':
                    clause_elements.append(_ModelEntity(i, self.ts_list))
                elif i.data == 'expression':
                    clause_elements.append(_Expression(i))
                elif i.data == 'term':
                    clause_elements.append(_Term(i))

            else:
                raise ValueError
        return clause_elements

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

            elif clause.data == 'expression':
                return self.reduce_expression(clause, ts_data)

            elif clause.data == 'term':
                return self.reduce_term(clause, ts_data)

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

    # def __str__(self):
    #     return str(self.clause)
    #
    # def __repr__(self):
    #     return self.__str__()


class _Expression(_Base):
    # type can be either 'numerical' for a pure expression
    #  or 'composite' for an expression where one of the operants
    #  is a model_entity

    def __init__(self, exprs):
        self.exprs = exprs

        if not isinstance(self.exprs, Tree):
            raise ValueError
        if self.exprs.data not in ['expression']:
            raise TypeError

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

    def _expression_string(self):
        for i in self.exprs.children:
            print(i)
        reduced = reduce(lambda x, y: f'{str(x)} {str(y)}', self.exprs.children)
        print('i am reduced', reduced)
        try:
            # first try to evaluate the experssion as python object
            evaluated = eval(reduced)
            if isinstance(evaluated, (float, int)):
                return Token('NUMBER', evaluated)
            else:
                return evaluated
        except NameError:
            return reduced

    # todo if a reduced expression is a number, make it a new token and return

    def __str__(self):
        return str(self._expression_string())

    def __repr__(self):
        return self.__str__()


class _ModelEntity:
    time_type = None

    def __init__(self, model_entity, ts_list):
        self.model_entity = model_entity
        self.ts_dct = ts_list

    @property
    def component_name(self):
        name = self.model_entity.children[0]
        assert name.type == 'NAME'
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

    def reduce(self):
        LOG.debug('model entity reduce invoked')
        time = eval(self.time)
        if isinstance(time, tuple):
            output = self.ts_dct[self.condition].simulate()[self.component_name].loc[float(time[0]): float(time[1])]
        else:
            output = self.ts_dct[self.condition].simulate()[self.component_name].loc[float(time)]
        LOG.debug('model entity reduce output is: ')
        LOG.debug(output)
        return output


class _Term:

    def __init__(self, term):
        self.term = term

    def __str__(self):
        return reduce(lambda x, y: f'{str(x)}{str(y)}', self.term.children)

    def __repr__(self):
        return self.__str__()

    def reduce(self):
        return eval(self.__str__())


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
