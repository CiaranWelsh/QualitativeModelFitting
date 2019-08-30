"""
todo write a docstring
todo all documentation
todo expand grammer to allow expressions
todo expand to steady state simulations as well
todo build in loops so we can do bulk validations
todo support events
"""
import logging

from qualitative_model_fitting._api import manual_interface
from qualitative_model_fitting._simulator import TimeSeries, TimeSeriesPlotter
from qualitative_model_fitting._parser import Parser
from qualitative_model_fitting._runner import ManualRunner
from qualitative_model_fitting._interpreter import Interpreter

LOGGING_LEVEL = logging.DEBUG

logging.basicConfig(filename='qmf_logger.log',
                    filemode='w',
                    level=LOGGING_LEVEL)





