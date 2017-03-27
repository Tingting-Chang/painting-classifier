#!/usr/bin/env python

import os, sys

import numpy as np
import pandas as pd

from keras.layers import Dense, Dropout, Embedding, Input, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import (MaxPooling2D, AveragePooling2D,
                        GlobalMaxPooling2D, GlobalAveragePooling2D)
from keras.optimizers import Adadelta
from keras.layers.merge import Concatenate
#from keras.regularizers import l2
from keras.models import Model
from keras import backend as K


def neural_net1(num_classes = 3, initial_rate=0.04,
            resized_filters1 = 32, resized_filters2 = 64, resized_filters3 = 48,
            resized_dense1 = 30, resized_dropout = 0.3,
            full1_filters1 = 32, full1_filters2 = 64,
            full1_filters3 = 48, full1_filters4 = 32,
            full1_dense1 = 100, full1_dropout = 0.3,
            combined_dense = 50, activations_conv = 'relu',
            activations_dense = 'relu'):
    ##########
    # Inputs #
    ##########
    image_full_input = Input(shape = (None, None, 3), name = 'full')
    image_resized_input = Input(shape = (200, 200, 3), name = 'resized_200')
    image_meta_input = Input(shape = (1,), name = 'metadata')
    
    ############################
    # Resized_200 convolutions #
    ############################
    resized_200 = Conv2D(resized_filters1, kernel_size = (4, 4), strides = (2, 2),
                         activation = activations_conv)(image_resized_input) #99*99*rf1
    resized_200_max = MaxPooling2D((3, 3), strides = (2, 2))(resized_200) #49*49*rf1
    resized_200_avg = AveragePooling2D((3, 3), strides = (2, 2))(resized_200) #49*49*rf1
    resized_200 = Concatenate()([resized_200_max, resized_200_avg]) #49*49*2rf1
    resized_200 = Conv2D(resized_filters2, kernel_size = (3, 3), strides = (2, 2),
                         activation = activations_conv)(resized_200) #24*24*rf2
    resized_200_max = MaxPooling2D((2, 2))(resized_200) #12*12*rf2
    resized_200_avg = AveragePooling2D((2, 2))(resized_200) #12*12*rf2
    
    #early_200_max = GlobalMaxPooling2D()(resized_200)
    #early_200_avg = GlobalAveragePooling2D()(resized_200)
    
    resized_200 = Concatenate()([resized_200_max, resized_200_avg]) #12*12*2rf2
    resized_200 = Conv2D(resized_filters3, kernel_size = (3, 3), strides = (1, 1),
                         activation = activations_conv)(resized_200) #10*10*rf3
    resized_200_max = MaxPooling2D((2, 2))(resized_200) #5*5*rf3
    average_200_avg = AveragePooling2D((2, 2))(resized_200) #5*5*rf3
    resized_200 = Concatenate()([resized_200_max, resized_200_avg]) #5*5*2rf3
    resized_200 = Flatten()(resized_200)
    resized_200 = Dense(resized_dense1, activation = activations_dense)(resized_200)
    resized_200 = Dropout(resized_dropout)(resized_200)
    
    ######################################
    # Full sized (cropped), first subnet #
    ######################################
    full1 = Conv2D(full1_filters1, kernel_size = (4, 4), strides = (2, 2),
                   activation = activations_conv)(image_full_input)
    full1_max = MaxPooling2D((3, 3), strides = (2, 2))(full1)
    full1_avg = AveragePooling2D((3, 3), strides = (2, 2))(full1)
    full1 = Concatenate()([full1_max, full1_avg])
    full1 = Conv2D(full1_filters2, kernel_size = (3, 3), strides = (2, 2),
                    activation = activations_conv)(full1)
    full1_max = MaxPooling2D((3, 3), strides = (2, 2))(full1)
    full1_avg = AveragePooling2D((3, 3), strides = (2, 2))(full1)
    
    #early_1_max = GlobalMaxPooling2D()(full1)
    #early_1_avg = GlobalAveragePooling2D()(full1)
    
    full1 = Concatenate()([full1_max, full1_avg])
    full1 = Conv2D(full1_filters3, kernel_size = (3, 3), strides = (2, 2),
                    activation = activations_conv)(full1)
    full1_max = MaxPooling2D((3, 3), strides = (2, 2))(full1)
    full1_avg = AveragePooling2D((3, 3), strides = (2, 2))(full1)
    full1g_max = GlobalMaxPooling2D()(full1)
    full1g_avg = GlobalAveragePooling2D()(full1)
    full1 = Concatenate()([full1_max, full1_avg])
    full1 = Conv2D(full1_filters4, kernel_size = (3, 3), strides = (2, 2),
                    activation = activations_conv)(full1)
    full1_max = GlobalMaxPooling2D()(full1)
    full1_avg = GlobalAveragePooling2D()(full1)
    full1 = Concatenate()([full1g_max, full1g_avg, full1_max, full1_avg])
    full1 = Dense(full1_dense1, activation = activations_dense)(full1)
    full1 = Dropout(full1_dropout)(full1)
    
    ############
    # Combined #
    ############
    combined = Concatenate()([resized_200, full1, image_meta_input])
    combined = Dense(combined_dense, activation = activations_dense)(combined)
    predictions = Dense(num_classes, activation = 'softmax')(combined)
    
    net = Model(inputs = [image_full_input, image_resized_input, image_meta_input],
                outputs = predictions)
    adadelta = Adadelta(lr = initial_rate)
    net.compile(optimizer = adadelta, loss = 'categorical_crossentropy',
                metrics = ['accuracy'])
    return net
