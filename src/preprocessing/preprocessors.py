import numpy as np

from datetime import datetime
import re, os

try:
    import cPickle as pickle
except:
    import pickle

class Preprocessor(object):

    def __init__(self):
        self._fitted = False
        
        self._pipelines = []
        self._base_pipeline_operations = []
        self._base_pipeline_loader = None
        self._base_pipeline_only_train = False
        self._cur_pipeline = None

    def with_pipeline(self, pipeline = None):
        self._cur_pipeline = pipeline
        return self

    def set_loader(self, loader, only_train = False, pipeline = None):
        if pipeline is None:
            pipeline = self._cur_pipeline
        if self._fitted:
            raise Exception('Cannot set loader to an already fitted preprocessor!')
        if not callable(loader):
            raise Exception('Loader must be callable!')
        if pipeline is None:
            self._base_pipeline_loader = loader
            self._base_pipeline_only_train = only_train
        if pipeline is None and len(self._pipelines) == 0:
            pipeline = 'main'
        if pipeline is not None:
            self._create_pipeline_if_necessary(pipeline)
            pipeline = [pipeline]
        else:
            pipeline = self._pipelines
        for p in pipeline:
            setattr(self, 'loader_' + p, loader)
            setattr(self, 'only_train_' + p, only_train)
        return self

    def add_operation(self, operation, pipeline = None):
        if pipeline is None:
            pipeline = self._cur_pipeline
        if self._fitted:
            raise Exception('Cannot add operations to an already fitted preprocessor!')
        methods = dir(operation)
        if 'fit' not in methods or 'transform' not in methods:
            raise Exception('operation must implement fit and transform methods!')
        if pipeline is None:
            self._base_pipeline_operations.append(operation)
        if pipeline is None and len(self._pipelines) == 0:
            pipeline = 'main'
        if pipeline is not None:
            if pipeline not in self._pipelines:
                self._create_pipeline_if_necessary(pipeline)
                return
            pipeline = [pipeline]
        else:
            pipeline = self._pipelines
        for p in pipeline:
            if not hasattr(self, 'operations_' + p):
                setattr(self, 'operations_' + p, [])
            getattr(self, 'operations_' + p).append(operation)
        return self

    def set_consumer(self, consumer, pipeline = None):
        if pipeline is None:
            pipeline = self._cur_pipeline
        if self._fitted:
            raise Exception('Cannot set consumer to an already fitted preprocessor!')
        if 'consume' not in dir(consumer):
            raise Exception('Consumer must implement consume method!')
        if pipeline is None:
            self._base_pipeline_operations.append(operation)
        if pipeline is None and (len(self._pipelines) or\
                len(self._pipelines) == 1 and self._pipelines[0] == 'main') == 0:
            pipeline = 'main'
        if pipeline is not None:
            if pipeline not in self._pipelines:
                self._create_pipeline_if_necessary(pipeline)
            pipeline = [pipeline]
        else:
            raise Exception('Cannot set consumer to all pipelines!')
        for p in pipeline:
            setattr(self, 'consumer_' + p, consumer)
        return self

    def load_and_transform(self, test = False, verbose = 0):
        if test and not self._fitted:
            raise Exception('Cannot transform a test set before the transforms are fitted!')
        if not self._pipelines:
            raise Exception('No loaders were set!')
        for pipeline in self._pipelines:
            if not hasattr(self, 'loader_' + pipeline):
                raise Exception('Pipeline ' + pipeline + ' has no loader!')
        loaded_data = {}
        for pipeline in self._pipelines:
            if test and getattr(self, 'only_train_' + pipeline):
                if verbose == 1:
                    print "Pipeline", pipeline, "ignored as it's only set for train data."
                continue
            if verbose == 1:
                print "Pipeline", pipeline, "started."
            data = getattr(self, 'loader_' + pipeline)(test)
            if verbose == 1:
                print "Pipeline", pipeline, "loaded."
            if hasattr(self, 'operations_' + pipeline):
                for operation in getattr(self, 'operations_' + pipeline):
                    if not test:
                        operation.fit(data)
                    data = operation.transform(data)
                    if verbose == 1:
                        print "Pipeline", pipeline + ':', "done", str(operation)
            if hasattr(self, 'consumer_' + pipeline):
                data = getattr(self, 'consumer_' + pipeline).consume(data, pipeline)
            if data is not None:
                loaded_data[pipeline] = data
            if verbose == 1:
                print "Pipeline", pipeline, "finished."
        if len(loaded_data) == 1:
            loaded_data = loaded_data[loaded_data.keys()[0]]
        self._fitted = True
        return loaded_data

    def _create_pipeline_if_necessary(self, pipeline):
        if pipeline not in self._pipelines:
            self._pipelines.append(pipeline)
            setattr(self, 'loader_' + pipeline, self._base_pipeline_loader)
            setattr(self, 'operations_' + pipeline,
                    [operator for operator in self._base_pipeline_operations])
            setattr(self, 'only_train_' + pipeline, self._base_pipeline_only_train)

    def save(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(file_name):
        result = None
        with open(file_name, 'rb') as f:
            result = pickle.load(f)
        return result
