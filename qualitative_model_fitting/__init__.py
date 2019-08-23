"""
todo write a docstring

"""
import logging

from qualitative_model_fitting import _suite
# do not move GLOBAL_TEST_SUITE from this line. Must come before
GLOBAL_TEST_SUITE = _suite.get_global_test_suite()

from qualitative_model_fitting._api import manual_interface
from qualitative_model_fitting._simulator import TimeSeries, TimeSeriesPlotter

LOGGING_LEVEL = logging.DEBUG

logging.basicConfig(filename='qmf_logger.log',
                    filemode='w',
                    level=LOGGING_LEVEL)





