import pandas as pd
import numpy as np
from PIL import Image
import re, sys, time, os
from keras.models import Sequential
from keras.layers import InputLayer, Convolution2D, MaxPooling2D, Dense, Dropout, Flatten, Merge
from keras.optimizers import Adadelta
import tensorflow as tf

import data_preparing


def neural_net_images(initial_rate=0.04, input_width=200, input_height=200):

	# image
	image = Sequential()
	image.add(InputLayer((input_width, input_height, 3), name = 'image'))  # 3*200*200
	image.add(Convolution2D(32, 5, 5, activation = 'relu')) # 32*196*196
	image.add(MaxPooling2D(pool_size = (2, 2))) #32*98*98
	image.add(Convolution2D(64, 5, 5, activation = 'relu')) # 64*94*94
	image.add(MaxPooling2D(pool_size=(2, 2))) # 64*47*47
	image.add(Dropout(0.2))
	image.add(Convolution2D(64, 4, 4, activation = 'relu')) # 64*44*44
	image.add(MaxPooling2D(pool_size = (2, 2))) #64*22*22
	image.add(Dropout(0.3))
	image.add(Flatten())

	img_size = Sequential()
	img_size.add(InputLayer((2, ), name = 'photo_stats'))
	
	img_merged = Sequential()
	img_merged.add(Merge([image, img_size], mode = 'concat')) #6043
	img_merged.add(Dense(1000, activation = 'relu')) # 1000
	img_merged.add(Dropout(0.5))
	img_merged.add(Dense(200, activation = 'relu')) # 200
	img_merged.add(Dense(2, activation = 'softmax')) 
	adadelta = Adadelta(lr = initial_rate)
	img_merged.compile(optimizers = adadelta, loss = 'categorical_crossentropy', metrics = ['accuracy'])

	return img_merged



def main():
	
	images_colors, images_stats = get_net_data()

	net = neural_net_images()
	history = net.fit({'images_colors': images_colors, 'images_stats': images_stats}, y, validation_split = 0.2)
	
	net_predicted = net.predict_classes({'images_colors': images_colors, 'images_stats': images_stats})
	net_evaluate = net.evaluate({'images_colors': images_colors, 'images_stats': images_stats}, y)

	net_predicted.to_csv('./data/net_predicted.csv')
	net_evaluate.to_csv('./data/net_evaluate.csv')


main()

