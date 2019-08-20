import os, glob
import pandas as pd
import numpy as np

from typing import Optional


class DictResults:
    """
    A dictionary like interface to a storage class for test results
    """
    _obs = {}

    def __init__(self):
        pass

    def __contains__(self, item):
        return item in self.__dict__

    def __getitem__(self, item):
        return self.__dict__.__getitem__(item)

    def __setitem__(self, key, value):
        if not isinstance(value, dict):
            raise AttributeError(f'Cannot set object of type "{type(value)}" '
                                 f'as value of a Result. Only dict objects are accepted.')
        self.__dict__[key] = value

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    @property
    def obs(self):
        return self._obs

    @obs.setter
    def obs(self, value):
        self._obs = value

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def to_df(self):
        df_dct = {}
        for k, v in self.items():
            obs_series = pd.Series(list(v.keys()))
            truth_series = pd.Series(list(v.values()))
            df = pd.DataFrame([obs_series, truth_series]).transpose()
            df.columns = ['observation', 'truth']
            df_dct[k] = df
        return pd.concat(df_dct)


class PandasResult(DictResults):

    """
    class may be deprecated.
    """

    def __init__(self):
        super(PandasResult, self).__init__()

    def __get__(self, obj_instance, owner_class):
        return self.df

    def _make_dataframe(self):
        """
        turn a dict into a properly formatted dataframe
        Returns:

        """
        df_dct = {}
        for k, v in self.items():
            obs_series = pd.Series(list(v.keys()))
            truth_series = pd.Series(list(v.values()))
            df = pd.DataFrame([obs_series, truth_series]).transpose()
            df.columns = ['observation', 'truth']
            df_dct[k] = df
        return pd.concat(df_dct)


class DashBoardResult(DictResults):
    """
    Produce flask server that displays all the results
    in the web with simulation plots.
    """

    def __init__(self):
        NotImplementedError('This is on the todo list')
