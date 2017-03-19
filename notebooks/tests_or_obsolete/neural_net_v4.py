import pandas as pd
import numpy as np
from PIL import Image
import re, sys, time, os
from keras.models import Sequential
from keras.layers import InputLayer, Convolution2D, MaxPooling2D, Dense, Dropout, Flatten, Merge
from keras.optimizers import Adadelta


def neural_net_images(initial_rate=0.04, output_classes = 3,input_width=200, input_height=200):

	# image
	image = Sequential()
	image.add(InputLayer((3, input_width, input_height), name = 'images_colors'))  # 3*200*200
	image.add(Convolution2D(32, 5, 5, activation = 'relu')) # 32*196*196
	image.add(MaxPooling2D(pool_size = (2, 2))) #32*98*98
	image.add(Convolution2D(64, 5, 5, activation = 'relu')) # 64*94*94
	image.add(MaxPooling2D(pool_size=(2, 2))) # 64*47*47
	image.add(Dropout(0.2))
	image.add(Convolution2D(64, 4, 4, activation = 'relu')) # 64*44*44
	image.add(MaxPooling2D(pool_size = (2, 2))) #64*22*22
	image.add(Dropout(0.3))
	image.add(Flatten()) #30976

	img_size = Sequential()
	img_size.add(InputLayer((2, ), name = 'images_stats'))
	
	img_merged = Sequential()
	img_merged.add(Merge([image, img_size], mode = 'concat')) #30978
	img_merged.add(Dense(1000, activation = 'relu')) # 1000
	img_merged.add(Dropout(0.5))
	img_merged.add(Dense(200, activation = 'relu')) # 200
	img_merged.add(Dense(output_classes, activation = 'softmax')) 
	adadelta = Adadelta(lr = initial_rate)
	img_merged.compile(optimizer = adadelta, loss = 'categorical_crossentropy', metrics = ['accuracy'])

	return img_merged



def train_network(data, epochs = 100):
	data = data.copy()
	y = data['response']
	painters = data['painters']
	del data['response']
	del data['painters']
	indices = data['indices']
	del data['indices']
	net = neural_net_images(output_classes = len(painters))
	history = net.fit(data, y, validation_split = 0.2,
			nb_epoch = epochs, batch_size = 64)
	
	net_predicted = net.predict_classes(data)
	net_evaluate = net.evaluate(data, y)

	pd.concat([indices.reset_index(drop = True), 
		pd.DataFrame({'prediction': [painters[x] for x in net_predicted]})], axis = 1).to_csv('./data/net_predicted.csv', index = False)

	return net, history, net_evaluate
