"""
todo write a docstring

"""
__all__ = ['_simulator', '_parser']
from qualitative_model_fitting._simulator import TimeSeries
from qualitative_model_fitting._parser import _Parser, Encoder
from qualitative_model_fitting._case import TestCase
from qualitative_model_fitting._test_factory import TestCase
from qualitative_model_fitting._runner import RunnerBase, AutomaticRunner, ManualRunner
from qualitative_model_fitting._suite import *

VERBOSE = False

















