import numpy as np
from pandas.io.json import read_json
from pandas import DataFrame, read_csv

from sklearn.utils import shuffle, resample

import re, os

class BasePandasLoader(object):

    def __init__(self, ftrain, ftest, sample = None):
        self.ftrain = ftrain
        self.ftest = ftest
        self.sample = sample
        self.clear()

    def __call__(self, test = False):
        if test:
            if self.test is None:
                self.test = self._load_dataframe(self.ftest)
            return self.test
        else:
            if self.train is None:
                self.train = self._load_dataframe(self.ftrain)
                if self.sample:
                    self.train = self.train.sample(self.sample)
            return self.train

    def select_loader(self, columns):
        return SelectorLoader(self, columns)

    @staticmethod
    def _load_dataframe(fname):
        raise NotImplementedError

    def clear(self):
        self.train = None
        self.test = None

    def __getstate__(self):
        # Make sure we're not pickling the dataframes
        odict = self.__dict__.copy()
        del odict['train']
        del odict['test']
        return odict

    def __setstate__(self, idict):
        self.__dict__.update(idict)
        self.clear()

class JSONLoader(BasePandasLoader):

    def __init__(self, ftrain = 'data/train.json', ftest = 'data/test.json',
                 sample = None):
        super(JSONLoader, self).__init__(ftrain, ftest, sample)

    @staticmethod
    def _load_dataframe(fname):
        df = read_json(os.path.expanduser(fname))
        return df

class CSVLoader(BasePandasLoader):
    @staticmethod
    def _load_dataframe(fname):
        return read_csv(os.path.expanduser(fname))

class SelectorLoader(object):
    # This class replaces a lambda expression, that I'm concerned would
    # break the pickling. Also, a normal function would not suffice
    # in that the state (columns) must be preserved.

    def __init__(self, loader, columns):
        self.loader = loader
        self.columns = columns

    def __call__(self, test = False):
        return self.loader(test)[self.columns]
