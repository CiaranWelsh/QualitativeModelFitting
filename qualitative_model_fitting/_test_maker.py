import os, glob

from qualitative_model_fitting import TimeSeries
from qualitative_model_fitting import TestCase

'''
The simulator will run all interval_time series at once then the test maker 
will distribute those dataframes along with conditions to test cases. 
the test cases will be collected into a suit and then executed by 
the runner

First get the text part of each statement
then refine the interval_time pount. 
then apply any functions 
then apply any math
'''


# todo make all test cases use a subclass of type metaclass to automatically register them into a collection
# test maker should have all the unit methods which will combine to make the necessary for each class
# Each statement should get its own class

class TestCaseMeta(type):
    pass


class TestMaker:

    def __init__(self, ant_str, inputs, time_start, time_end, steps):
        self.ant_str = ant_str
        self.inputs = inputs
        self.time_start = time_start
        self.time_end = time_end
        self.steps = steps

        self.time_series_data = self._run_timeseries()

        # cls = type('A', (TestCase,), {'__doc__': 'class created by type'})
        # print(dir(cls))

    def _run_timeseries(self):
        return TimeSeries(
            self.ant_str, self.inputs,
            self.time_start, self.time_end, self.steps
        ).simulate()

    def create_test_cases(self):
        cls_list = []
        for condition_name, condition_dict in self.inputs.items():
            data = self.time_series_data[condition_name]
            obs = condition_dict['obs']
            cls = type(
                condition_name,
                (TestCase,),
                {
                    'data': data,
                    'obs': obs,
                 }
            )
            cls_list.append(cls)
        return cls_list

# class BaseClass(object):
#     def __init__(self, classtype):
#         self._type = classtype
#
# def ClassFactory(name, argnames, BaseClass=BaseClass):
#     def __init__(self, **kwargs):
#         for key, value in kwargs.items():
#             # here, the argnames variable is the one passed to the ClassFactory call
#             if key not in argnames:
#                 raise TypeError(f"Argument {key} not valid for {self.__class__.__name__}")
#             setattr(self, key, value)
#         BaseClass.__init__(self, name)
#     newclass = type(name, (BaseClass,),{"__init__": __init__})
#     return newclass
#
# s = ClassFactory('cheese', 'arguments'.split())
# print(s)
# print(s.mro())
# print(s.__init__(BaseClass))
# print(dir(s))
