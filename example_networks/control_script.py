import os, glob
import pandas as pd
import numpy as np
from collections import OrderedDict

import qualitative_model_fitting as qmf
from example_networks.model_strings import model_string
from example_networks import WD, PLOTS_DIR
import logging

LOG = logging.getLogger(__name__)


string = """

timeseries InsulinOnly {Insulin=1} 0, 100, 101

observation
    obs1: IRS1a[InsulinOnly]@t=0 < IRS1a[InsulinOnly]@t=10 
    // obs2: IRS1a[InsulinOnly]@t=0 < IRS1a[InsulinOnly]@t=10 

"""

if __name__ == '__main__':
    res = qmf.manual_interface(model_string, string)
    print(res)

