from types import MethodType
from collections import OrderedDict

import pandas as pd
import numpy as np
from qualitative_model_fitting import _Parser


class TestCase:

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

    def __init__(self):
        self.statements = self._encode_obs()
        # make copy for preservatin of original data frame
        self.data_copy = self.data.copy()

    def _encode_obs(self):
        p = _Parser(self.obs)
        return p.statements

    def dispatcher(self, variable_name, matches, encoded):
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
            print('match:', m, 'e', e)
            if e is 1:
                # this means that the next element is either a interval_time digit or a interval_time interval
                time_symbol_encountered = True
                print('time symbol encountered')
                continue
            # 2 in funct
            elif e is 2:
                function_encountered = True
                # save for later
                funct = m#self.function_modifier(m, variable_name, )
                # print('fun ct', func)
            # 3 is text
            elif e is 3:
                s += self.text(m, variable_name)
            # 4 is digit
            elif e is 4:
                if time_symbol_encountered:
                    print('from point time. time symbol is {}'.format(time_symbol_encountered))
                    s += self.point_time(int(m), variable_name)
                elif numerical_operator_encountered:
                    print('from point time. numerical op flag is {}'.format(numerical_operator_encountered))
                    # could convert division to 1/x to prevent need for ordering?
                    s += self.mathematical_operator(variable_name, numerical_operator, m)
                elif not numerical_operator_encountered:
                    print('from point time. numerical op flag is {}'.format(numerical_operator_encountered))
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
                print('encountered numerical operator')
                # reset time flag
                time_symbol_encountered = False
            else:
                raise ValueError('we have a problem')
        # copy back to original dataframe.
        # this is a problem because the code doesn't get EXECUTED here
        # self.data = self.data_copy.copy()
        return s, funct

    def make_test(self):
        test_methods = OrderedDict()
        for i in range(self.statements.shape[0])[:1]:
            encoded = self.statements['encoded'].iloc[i]
            matches = self.statements['matches'].iloc[i]
            print(encoded)
            print(matches)

            operator_ids = [i for i in encoded if i is 6]
            if len(operator_ids) != 1:
                raise SyntaxError('Only 1 mathematical_operator is allowed in each '
                                  'statement. {} seems'
                                  ' to have {}'.format(matches, len(operator_ids)))
            operator_index = encoded.index(self.labels['mathematical_operator'])
            clause1_matches = matches[:operator_index]
            clause1_encoded = encoded[:operator_index]
            clause2_matches = matches[operator_index+1:]
            clause2_encoded = encoded[operator_index+1:]
            operator_match = matches[operator_index]
            operator_encoded = encoded[operator_index]

            clause1, clause1_func = self.dispatcher('clause1', clause1_matches, clause1_encoded)
            clause2, clause2_func = self.dispatcher('clause2', clause2_matches, clause2_encoded)
            compare_statement = self.compare(operator_match, clause1_func, clause2_func)

            method_name = f'test_statement_{i}'
            s = 'import pandas as pd\n'
            s += 'import numpy as np\n'
            s += f'def {method_name}(self):\n'
            s += clause1 +'\n'
            s += clause2 +'\n'
            s += compare_statement +'\n'
            print(s)
            # render the staticmethod from string s and store in __dict__
            exec(s, self.__dict__)
            # exec(, self.__dict__, {'pd': pd, 'np': np})
            test_methods[method_name] = self.__dict__[method_name]
        return test_methods


    @staticmethod
    def text(text, data_variable_name=None):
        """
        Deal with text variables by pulling out the correct data column

        The problem with this is that it actually does the work
        whereas I need the blueprint to do the work.

        Do I need to make_test each clause separetly?
        Get the index of the number 6. Need to ensure no
        multiple number 6 is present. Then split the list on the index
        of number 6.
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
        print('start is: ', start)
        print('end is: ', end)
        if data_variable_name is None:
            data_variable_name = 'self.data'
        s = f"    {data_variable_name} = {data_variable_name}.loc[{start}: {end}, ]\n    print({data_variable_name})\n"
        return s

    @staticmethod
    def point_time(time, data_variable_name=None):
        print('we have point time')
        if data_variable_name is None:
            data_variable_name = 'self.data'
        return f"    {data_variable_name} = float({data_variable_name}.loc[{time}])\n    print({data_variable_name})"

    @staticmethod
    def compare(operator, clause1_funct, clause2_funct):
        print('a now we compare')
        print('c1', clause1_funct)
        print('c2', clause2_funct)
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
        print('now is a func')
        if data_variable_name is None:
            data_variable_name = 'self.data'
        return f"    {data_variable_name} = {data_variable_name}({function})\n    print({data_variable_name})\n"

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
