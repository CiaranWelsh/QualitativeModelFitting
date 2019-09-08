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


OPTIONS = dict(
    logging=dict(
        level=dict(
            fh=logging.DEBUG,
            ch=logging.DEBUG,
        ),
        use_file_logger=True,
        use_console_logger=True,
        filename='qmf_file_logger.log',
    )
)

def logging_config():
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(name)s - %(funcName)s - %(levelname)s: %(message)s')
    if OPTIONS['logging']['use_file_logger']:
        fh = logging.FileHandler(OPTIONS['logging']['filename'])
        fh.setLevel(OPTIONS['logging']['level']['fh'])
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # create console handler with a higher log level
    if OPTIONS['logging']['use_console_logger']:
        ch = logging.StreamHandler()
        fh.setLevel(OPTIONS['logging']['level']['ch'])
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    # create formatter and add it to the handlers
    # add the handlers to the logger
    return logger

LOG = logging_config()




