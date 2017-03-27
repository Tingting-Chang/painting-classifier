import numpy as np
from pandas.io.json import read_json
from pandas import DataFrame, get_dummies, read_csv

from sklearn.utils import shuffle, resample

from datetime import datetime
import re, os

from PIL import Image

try:
    import cPickle as pickle
except:
    import pickle

class BasePipelineMerger(object):
    '''
    Subclasses must implement do_merge(self, test = False) that would set
    how to combine data from self.data.
    '''
    def __init__(self, input_pipelines):
        self.input_pipelines = input_pipelines
        self.data = {}

    def consume(self, data, pipeline):
        self.data[pipeline] = data

    def do_merge(self, test = False):
        raise NotImplementedError

    def __call__(self, test = False):
        return self.do_merge(test)

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['data']
        return odict

    def __setstate__(self, idict):
        self.__dict__.update(idict)
        self.data = {}

class PandasColumnMerger(BasePipelineMerger):

    def __init__(self, input_pipelines, on = None, how = 'outer'):
        super(PandasColumnMerger, self).__init__(input_pipelines)
        self.on = on
        self.how = how

    def do_merge(self, test = False):
        if self.on:
            df = self.data[self.input_pipelines[0]]
            for pipeline in self.input_pipelines[1:]:
                df = df.merge(self.data[pipeline], how = self.how,
                              on = self.on)
            return df
        else:
            return pd.concat(self.data.values(), axis = 1)

class SimpleDataRelay(object):
    def __init__(self):
        self.data = None
    
    def consume(self, data, pipeline):
        self.data = data
    
    def __call__(self, test = False):
        return self.data
    
    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['data']
        return odict

    def __setstate__(self, idict):
        self.__dict__.update(idict)
        self.data = {}
