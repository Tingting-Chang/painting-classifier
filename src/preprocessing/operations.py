import numpy as np
from pandas import get_dummies

from sklearn.utils import shuffle, resample

import re, os

# from PIL import Image

class Selector(object):
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, data):
        pass

    def transform(self, data):
        return data[self.columns]

class ColumnDrop(object):
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, data):
        pass

    def transform(self, data):
        return data.drop(self.columns, axis = 1)

class ToNdarray(object):
    def __init__(self, dtype = np.float32, outshape = None):
        self.dtype = dtype
        self.outshape = outshape
    
    def fit(self, data):
        pass

    def transform(self, data):
        data = np.array(data, dtype = self.dtype)
        if self.outshape:
            data = data.reshape(self.outshape)
        return data

class Slicer(object):
    def __init__(self, rowslice, colslice):
        self.rowslice = rowslice
        self.colslice = colslice
    
    def fit(self):
        pass
    
    def transform(self, data):
        return data[rowslice, colslice]

'''
class PhotoLoaderGenerator(object):
    def __call__(self, data):
        images = np.zeros((data.shape[0], 3, 100, 100), dtype = np.float32)
        for i, row in enumerate(data.iterrows()):
            images[i] = _get_image(row[1]['listing_id'], row[1]['photo_name'])
        images = images / 255.0
        return images

def _get_image(listing_id, photo_name):
    if len(photo_name) == 0:
        return np.zeros((3, 100, 100))
    path = 'data/images_compressed/%d/%d/%s' % (listing_id / 1000,
                    listing_id, photo_name)
    im = Image.open(path)
    pixels = np.array(im.getdata()).reshape(10000, -1).swapaxes(0, 1).reshape(-1, 100, 100)
    if pixels.shape[0] == 1:
        pixels = np.repeat(pixels, 3, axis = 0)
    return pixels.astype(np.float32)'''

class LambdaApplier(object):
    def __init__(self, column, operations):
        self.operations = operations
        self.column = column

    def fit(self, data):
        pass

    def transform(self, data):
        for name in self.operations:
            data[name] = data[self.column].apply(self.operations[name])
        return data

class Dummifier(object):
    
    def __init__(self, output_cols = None, **kwargs):
        self.output_cols = output_cols
        self.kwargs = kwargs
        self.output_cols_fitted = None
    
    def fit(self, data):
        if self.output_cols is None:
            self.output_cols_fitted = list(set(data))
            self.output_cols_fitted.sort()
    
    def transform(self, data):
        dummies = get_dummies(data, **(self.kwargs))
        if self.output_cols:
            return dummies[self.output_cols]
        else:
            return dummies[self.output_cols_fitted]
    
    def get_output_columns(self):
        return self.output_cols if self.output_cols is not None else self.output_cols_fitted

class SeriesDummifier(Dummifier):
    def __init__(self):
        self.output_cols = None
        self.kwargs = {}
        self.output_cols_fitted = None
        self.categories_counts = None
    
    def fit(self, data):
        self.categories_counts = data.value_counts()
        self.output_cols = list(self.categories_counts.index)
        
    def get_counts(self):
        return self.categories_counts

class CategoricalMapper(object):
    
    def __init__(self, column, top_categories = 3, inplace = True,
                    include_others = False):
        self.top_categories = top_categories
        self.column = column
        self.inplace = inplace
        self.include_others = include_others
    
    def fit(self, data):
        counts = data[self.column].value_counts()
        self.category_mapper = dict(zip(counts.index[:self.top_categories],
                                    range(1, self.top_categories + 1)))
    
    def transform(self, data):
        if not self.inplace:
            data = data.copy()
        data[self.column] = data[self.column].apply(lambda key: self.category_mapper.get(key, 0))
        if not include_others:
            data = data[data[self.column] != 0]
        return data

class CategoricalFilter(object):
    
    def __init__(self, column, top_categories = 3):
        self.top_categories = top_categories
        self.column = column
    
    def fit(self, data):
        self.classes = data[self.column].value_counts().index[:self.top_categories]
    
    def transform(self, data):
        return data[data[self.column].isin(self.classes)]

class LogTransform(object):
    
    def __init__(self, cols = None):
        self.cols = cols
    
    def fit(self, data):
        pass
    
    def transform(self, data):
        if self.cols:
            data[self.cols] = data[self.cols].applymap(lambda x: np.log(x+1))
            return data
        else:
            return data.applymap(lambda x: np.log(x+1))

class GroupByAggregate(object):
    
    def __init__(self, by, aggregator, reset_index = True):
        self.by = by
        self.aggregator = aggregator
        self.reset_index = reset_index
    
    def fit(self, data):
        pass
    
    def transform(self, data):
        result = data.groupby(self.by).aggregate(self.aggregator)
        if self.reset_index:
            return result.reset_index()
        else:
            return result

class FillNA(object):
    
    def __init__(self, fill_value = 0.0, subset = None):
        self.fill_value = fill_value
    
    def fit(self, data):
        pass
    
    def transform(self, data):
        return data.fillna(self.fill_value)

class SeparateDictKey(object):
    
    def __init__(self, key_to_separate):
        self.key = key_to_separate
    
    def __call__(self, data):
        if self.key in data:
            y = data[self.key]
            del data[self.key]
            return data, y
        else:
            return data
