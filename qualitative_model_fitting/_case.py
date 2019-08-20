from types import MethodType
from collections import OrderedDict

import pandas as pd
import numpy as np
from qualitative_model_fitting import _Parser
from qualitative_model_fitting._suite import Suite, GLOBAL_TEST_SUITE


class TestCaseMeta(type):
    """
    Classes of type TestCaseMeta are like regular classes but they
    are automatically registered into a variable stored in
    qualitative_model_fitting._suite.GLOBAL_TEST_SUITE.
    """
    def __new__(cls, clsname, bases, attrs):
        newclass = super(TestCaseMeta, cls).__new__(cls, clsname, bases, attrs)
        cls._register_cls(newclass)
        return newclass

    def _register_cls(cls):
        """
        Adds created classes to the GLOBAL_TEST_SUITE. Does not
        include the parent class _case.TestCase.

        Returns:

        """
        # import here to avoid UnboundLocalError
        from qualitative_model_fitting._suite import GLOBAL_TEST_SUITE
        # do not add _case.TestCase to register
        if cls.__name__ != 'TestCase':
            GLOBAL_TEST_SUITE.append(cls)
        return GLOBAL_TEST_SUITE


class TestCase(metaclass=TestCaseMeta):
    """
    Parent class of all tests. A TestCase understands user input
    via the Parser and pieces together a function that tests
    each observation.
    """
    # variables are filled by TestMaker
    data = None
    obs = None

    # order of eval = text, interval_time, func, exprs
    precidence = [3, 1, 2, 7]

    if data is not None:
        if not isinstance(data, pd.DataFrame):
            raise TypeError

    test_methods = OrderedDict()

    labels = {
        'time_symbol': 1,
        'func': 2,
        'text': 3,
        'digit': 4,
        'interval': 5,
        'mathematical_operator': 6,
        'math_operator': 7,
    }
    obs = None
    data = None

    def __init__(self):
        self.statements = self._encode_obs()
        # make copy for preservatin of original data frame
        self.data_copy = self.data.copy()

        for i in [self.obs, self.data]:
            if i is None:
                raise AttributeError(f'The "{i}" attribute is None, '
                                     'please set with an appropriate value')
        self.tests = self.make_tests()

    def __get__(self, item):
        if item not in self.__dict__:
            raise AttributeError(f'item "{item}" is not an attribute of class "{self.__name__}"')
        return self.__dict__[item]

    def _encode_obs(self) -> list:
        """
        Uses the parser to encode user inputs for easier interpretation of
        which rules to use

        Returns:

        """
        p = _Parser(self.obs)
        return p.statements

    def dispatch(self, variable_name, matches, encoded) -> tuple:
        """
        Determine which methods are needed to test observation. This mechanism
        of creating TestCases is in its beta stage of development and may be
        subject to change to increase flexibility.

        Args:
            variable_name: Usually clause1 or clause2
            matches: Elements of statement matched by regular expressions
            encoded: The encoded version of matches.

        Returns: tuple(string, function)

        """
        s = ''
        time_symbol_encountered = False
        function_encountered = False
        numerical_operator_encountered = False
        numerical_operator = None
        funct = None
        while matches:
            e = encoded.pop(0)
            m = matches.pop(0)
            # when interval_time symbol enountered, set to True, digit behaves like a interval_time point
            # when when False, digit behaves like a constant in an expression
            # interval_time symbol
            # 1 is interval_time
            # print('match:', m, 'e', e)
            if e is 1:
                # this means that the next element is either a interval_time digit or a interval_time interval
                time_symbol_encountered = True
                # print('time symbol encountered')
                continue
            # 2 in funct
            elif e is 2:
                function_encountered = True
                # save for later
                funct = m  # self.function_modifier(m, variable_name, )
                # print('fun ct', func)
            # 3 is text
            elif e is 3:
                s += self.text(m, variable_name)
            # 4 is digit
            elif e is 4:
                if time_symbol_encountered:
                    # print('from point time. time symbol is {}'.format(time_symbol_encountered))
                    s += self.point_time(int(m), variable_name)
                elif numerical_operator_encountered:
                    # print('from point time. numerical op flag is {}'.format(numerical_operator_encountered))
                    # could convert division to 1/x to prevent need for ordering?
                    s += self.mathematical_operator(variable_name, numerical_operator, m)
                elif not numerical_operator_encountered:
                    # print('from point time. numerical op flag is {}'.format(numerical_operator_encountered))
                    s += self.simple_expression(m, data_variable_name=variable_name)
                    # s += self.expression()
                # reset time flag
                time_symbol_encountered = False
            # 5 is interval
            elif e is 5:
                start, end = eval(m)
                s += self.interval_time(start, end, variable_name)
                function_encountered = False
            # 6 is mathematical_operator (comparative mathematical_operator)
            elif e is 6:
                s += self.compare(m)
            # 7 is numerical mathematical_operator
            elif e is 7:
                numerical_operator_encountered = True
                numerical_operator = m
                # print('encountered numerical operator')
                # reset time flag
                time_symbol_encountered = False
            else:
                raise ValueError('we have a problem')
        return s, funct

    def make_tests(self) -> dict:
        """
        Calls the :py:meth:`dispatch` method on each user input.

        Returns:

        """
        test_methods = OrderedDict()
        for i in range(self.statements.shape[0]):
            encoded = self.statements['encoded'].iloc[i]
            matches = self.statements['matches'].iloc[i]
            # print(encoded)
            # print(matches)

            operator_ids = [i for i in encoded if i is 6]
            if len(operator_ids) != 1:
                raise SyntaxError('Only 1 mathematical_operator is allowed in each '
                                  'statement. {} seems'
                                  ' to have {}'.format(matches, len(operator_ids)))
            operator_index = encoded.index(self.labels['mathematical_operator'])
            clause1_matches = matches[:operator_index]
            clause1_encoded = encoded[:operator_index]
            clause2_matches = matches[operator_index + 1:]
            clause2_encoded = encoded[operator_index + 1:]
            operator_match = matches[operator_index]
            operator_encoded = encoded[operator_index]

            clause1, clause1_func = self.dispatch('clause1', clause1_matches, clause1_encoded)
            clause2, clause2_func = self.dispatch('clause2', clause2_matches, clause2_encoded)
            compare_statement = self.compare(operator_match, clause1_func, clause2_func)

            method_name = f'test_statement_{i}'
            s = 'import pandas as pd\n'
            s += 'import numpy as np\n'
            s += f'def {method_name}(self):\n'
            s += clause1 + '\n'
            s += clause2 + '\n'
            s += compare_statement + '\n'
            # render the staticmethod from string s and store in __dict__
            exec(s, self.__dict__)
            # bind the newly defined function to self (necessary to prevent the need
            # for passing self as first argument
            self.__dict__[method_name] = self.__dict__[method_name].__get__(self, method_name)
            # store handle in another dict for easy retrieval later
            test_methods[method_name] = self.__dict__[method_name]
        return test_methods

    @staticmethod
    def text(text, data_variable_name=None):
        """

        :return:
        """
        if data_variable_name is None:
            data_variable_name = 'self.data'
        return f"    {data_variable_name} = self.data['{text}']\n"

    @staticmethod
    def digit():
        pass

    @staticmethod
    def interval_time(start, end, data_variable_name=None):
        # a comparison cannot be able between two intervals of different lengths
        # print('start is: ', start)
        # print('end is: ', end)
        if data_variable_name is None:
            data_variable_name = 'self.data'
        s = f"    {data_variable_name} = {data_variable_name}.loc[{start}: {end}, ]\n"
        return s

    @staticmethod
    def point_time(time, data_variable_name=None):
        # print('we have point time')
        if data_variable_name is None:
            data_variable_name = 'self.data'
        return f"    {data_variable_name} = float({data_variable_name}.loc[{time}])\n"

    @staticmethod
    def compare(operator, clause1_funct, clause2_funct):
        # print('a now we compare')
        # print('c1', clause1_funct)
        # print('c2', clause2_funct)
        clause1 = f'clause1.{clause1_funct}()' if clause1_funct else 'clause1'
        clause2 = f'clause2.{clause2_funct}()' if clause2_funct else 'clause2'
        s = f"    boolean = {clause1} {operator} {clause2}\n"
        s += f"    if isinstance(boolean, (pd.Series)) and len(boolean) > 1:\n"
        s += f"        raise ValueError('The truth value of an array is ambiguous. " \
             f"Please use the any or all modifiers to clarify how you wish to evaluate test.')\n"
        s += f"    return boolean\n"
        return s

    @staticmethod
    def function_modifier(function, data_variable_name=None):
        # print('now is a func')
        if data_variable_name is None:
            data_variable_name = 'self.data'
        return f"    {data_variable_name} = {data_variable_name}({function})\n"

    @staticmethod
    def mathematical_operator(left, operator, right):
        return f"    {left} = {left} {operator} {right}\n"

    @staticmethod
    def simple_expression(expression, operator=None, data_variable_name=None):
        if data_variable_name is None:
            data_variable_name = 'self.data'
        if operator is not None:
            return f"    {data_variable_name} = {data_variable_name} {operator} {expression}\n"
        else:
            return f"    {data_variable_name} = {expression}\n"

    def __str__(self):
        s = self.statements['statement'].tolist()
        s = '\n'.join(s)
        classname = self.__class__.__name__ + '\n' + '-' * len(self.__class__.__name__)
        return f'{classname}\n{s}'

    def __repr__(self):
        return self.__str__()