import os, glob
import numpy as np
import pandas as pd
import unittest


class RunnerBase:

    def __init__(self, suite):
        self.suite = suite


class ManualRunner(RunnerBase):
    pass


class AutomaticRunner(RunnerBase):
    pass

