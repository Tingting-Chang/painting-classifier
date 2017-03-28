
import pandas as pd
import numpy as np
from PIL import Image
from sklearn import preprocessing
import sys, os, re

IMAGES_PATH = 'data/images_athenaeum'
NUM_CHANNELS = 3

MIN_DIMS = 64

def get_image_path(author_id, painting_id, thumb = 'full'):
    return os.path.join(IMAGES_PATH, thumb, str(author_id), str(painting_id) + '.jpg')

def get_image_array(author_id, painting_id, thumb = 'full'):
    image_path = get_image_path(author_id, painting_id, thumb)
    im = Image.open(image_path)
    if min(im.width, im.height) < MIN_DIMS:
        image_path = get_image_path(author_id, painting_id)
        im = Image.open(image_path)
        if min(im.width, im.height) < MIN_DIMS:
            ratio = float(MIN_DIMS) / min(im.width, im.height)
            im = im.resize((int(im.width * ratio), int(im.height * ratio)), Image.LANCZOS)
    return np.array(im.getdata(), dtype = np.float32).reshape(1, im.width, im.height, NUM_CHANNELS) / 255
	
def random_crop(np_image, width, height):
    x_offset = np.random.randint(np_image.shape[1] - width + 1)
    y_offset = np.random.randint(np_image.shape[2] - height + 1)
    return np_image[:, x_offset:(x_offset + width), y_offset:(y_offset + height)]

def get_image_crops_batch(list_ids, dict_sizes):
    full_sized = [get_image_array(*id_) for id_ in list_ids]
    result = {}
    for size_name, size in dict_sizes.items():
        width = size[0]
        if width is None:
            width = min([image.shape[1] for image in full_sized])
        height = size[1]
        if height is None:
            height = min([image.shape[2] for image in full_sized])
        result[size_name] = np.vstack([
                random_crop(image, width, height) for image in full_sized])
    return result

#def get_image_crop_batch_from_df(df, dict_sizes):
    #list_paths = [get_image_path(row['author_id'], row['painting_id'])
                  #for pos, row in df.iterrows()]
    #return get_image_crops_batch(list_paths, dict_sizes)

def get_image_thumb_batch_from_df(df, thumb):
    list_ids = [(row['author_id'], row['painting_id'], thumb)
                  for pos, row in df.iterrows()]
    return get_image_crops_batch(list_ids, {thumb: (None, None)})[thumb]

class HeightWidthRatio(object):
    def fit(self, data):
        pass
    
    def transform(self, data):
        data['height_width_ratio'] = data['height_px'].astype(np.float) / data['width_px']
        return data

class ImageLoaderGenerator(object):
    def __init__(self, thumb):
        self.thumb = thumb
    
    def __call__(self, data):
        return get_image_thumb_batch_from_df(data, self.thumb)

