#!/usr/bin/env python
import urllib
import pandas as pd
import numpy as np
from PIL import Image
import re, sys, time, os
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import InputLayer, Convolution2D, MaxPooling2D, Dense, Dropout, Flatten, Merge
from keras.optimizers import Adadelta
import tensorflow as tf

from google.cloud import storage
from StringIO import StringIO

PROJECT_NAME = 'painting-classifier'
BUCKET_NAME = 'painting-classifier-data'

bucket = storate.Client(project = PROJECT_NAME).bucket(BUCKET_NAME)

def get_sizes_painting(df_data, image_dir):
	sizes = []
	processed = 0
	for img_fn in df_data.file_name:
	    im = Image.open(image_dir + img_fn)
	    sizes.append([im.width, im.height, im.layers])
	    processed += 1
	    if processed % 100 == 0:
	        if processed % 1000 == 0:
	            sys.stdout.write('|')
	        else:
	            sys.stdout.write('.')
	        sys.stdout.flush()
	sizes = pd.DataFrame(sizes, columns = ['width', 'height', 'layers'])

	return sizes



def neural_net_photo_version2(initial_rate=0.04):
    photo = Sequential()
    photo.add(InputLayer((200, 200, 3), name = 'photo')) #3*200*200
    photo.add(Convolution2D(32, 5, 5, activation = 'relu')) #32*196*196
    photo.add(MaxPooling2D(pool_size = (2, 2))) #32*98*98
    photo.add(Convolution2D(64, 5, 5, activation = 'relu')) #64*94*94
    photo.add(MaxPooling2D(pool_size = (2, 2))) #64*47*47
    photo.add(Dropout(0.2))
    photo.add(Convolution2D(64, 4, 4, activation = 'relu')) #64*44*44
    photo.add(MaxPooling2D(pool_size = (2, 2))) #64*22*22
    photo.add(Dropout(0.3))
    photo.add(Flatten())
    img_size = Sequential()
    img_size.add(InputLayer((2,), name = 'photo_stats'))
    img_merged = Sequential()
    img_merged.add(Merge([photo, img_size], mode = 'concat')) #6403
    img_merged.add(Dense(1000, activation = 'relu')) #1000
    img_merged.add(Dropout(0.5))
    img_merged.add(Dense(200, activation = 'relu')) #200
    img_merged.add(Dense(2, activation = 'softmax'))
    adadelta = Adadelta(lr = initial_rate)
    img_merged.compile(optimizer = adadelta, loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return img_merged



def images_colors(file_names, image_dir):
    #CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    photos = []
    format_str = ERASE_LINE + '\rLoading images: %d/%d'
    total_photos = len(file_names)
    processed = 0
    for img_fn in file_names:
	try:
	    photo_pixels = get_image_data('resized_200/' + img_fn)
	    photos.append(photo_pixels)
	    processed += 1
	    sys.stdout.write(format_str % (processed, total_photos))
	    sys.stdout.flush()
	except BaseException as e:
	    sys.stderr.write('Error loading photo %s\n%s\n' % (img_fn, e))
	    sys.stderr.flush()
	sys.stdout.write('\n')
    photos = np.vstack(photos) / 255

    return photos

def get_image_data(image_path):
    im = Image.open(StringIO(bucket.blob(image_path).download_as_string()))
    return np.array(im.getdata(), dtype = np.float32).reshape(1, im.height, im.width, -1) + np.zeros((1, 1, 1, 3))

def run():
	# get your data
	painting_info_clean = pd.read_csv('./data/painting_info_clean.csv')
	df_data = painting_info_clean[painting_info_clean.short_name.isin(['gogh_van', 'rubens'])]

	y = pd.get_dummies(df_data.short_name)
	dummies_cols = y.columns
	y = np.array(y, dtype = np.float32)

	sizes_paintings = pd.read_csv('data/images_sizes_2325.csv')
	sizes_paintings = pd.merge(df_data[['file_name']], sizes_paintings, how = 'left', on='file_name')
	photo_stats = np.array(sizes_paintings[['width', 'height']], dtype = np.float32)

	# balance image data: width, height
	scaler = preprocessing.StandardScaler().fit(photo_stats)
	photo_stats = scaler.transform(photo_stats)

	photos = images_colors(df_data['file_name'], 'data/resized_200/')

	net = neural_net_photo_version2()

	history2 = net.fit({'photo': photos, 'photo_stats': photo_stats}, y, validation_split = 0.2)
	net.predict_classes({'photo': photos, 'photo_stats': photo_stats})
	net.evaluate({'photo': photos, 'photo_stats': photo_stats}, y)
