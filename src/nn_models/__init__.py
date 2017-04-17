#!/usr/bin/env python
import os, sys

import numpy as np
import pandas as pd

from keras.models import load_model
from keras.callbacks import CSVLogger, ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
#from ..enqueuer import Enqueuer



def fit_generator(net, train_generator, valid_generator = None, plot=False,
                        epochs=3000, save_to='nn_trained',
                        lr_reduce_after = 20, early_stopping = 50,
                        nb_worker = 5, max_q_size = 10, class_counts = None):
    
    '''Trains a neural network by using batch generation.
        
    Arguments:
    net -- (keras.model) The neural network to be fitted.
    train_generator -- (iterator) Iterator that generates batches for training.
        It should return a (X, y) tuple
    valid_generator -- (iterator, None) Similar to train_generator, if validation
        data is desired
    plot -- (bool, False) if true, a plot of the training and validation
        errors at the end of each epoch will be shown once the network
        finishes training.
    epochs -- (int, 3000) the maximum number of epochs for which the
        network should train.
    save_to -- (str, 'nn_trained') name of the directory in which the
        training history and network are saved.
    lr_reduce_after -- (int, 20) number of epochs of no improvements after which
        the learning rate should be reduced
    early_stopping -- (int, 50) number of epochs of no improvements after which
        the training should stop
    nb_worker -- (int, 5) number of threads to be used on train/validation batch
        generation
    max_q_size -- (int, 10) maximum number of batches generated at a time
    class_counts -- (Numpy Array or Pandas Series, None) the bin counts for
        all the elements in each class. If provided, the training will be balanced
    '''
    
    if not os.path.exists(save_to):
        os.makedirs(save_to)
    save_to = save_to + '/'
    
    earlystopping = EarlyStopping(patience = early_stopping)
    checkpoint = ModelCheckpoint(save_to + 'net.h5', save_best_only = True)
    logger = CSVLogger(save_to + 'history.log')
    lrreducer = ReduceLROnPlateau(factor = 0.2, patience = lr_reduce_after)
    callbacks = [checkpoint, logger, earlystopping, lrreducer]
    
    #enqueued_train_generator = Enqueuer(train_generator, workers = nb_worker,
                #max_q_size = max_q_size)
    #enqueued_train_generator.start()

    #if valid_generator:
        #enqueued_valid_generator = Enqueuer(valid_generator, workers = nb_worker,
                #max_q_size = max_q_size)
        #enqueued_valid_generator.start()
    #else:
        #enqueued_valid_generator = None
    
    if class_counts is not None:
        class_weights = dict(zip(range(len(class_counts)), get_balanced_class_weights(class_counts)))
    else:
        class_weights = None
    
    history = net.fit_generator(train_generator, steps_per_epoch = train_generator.n_batches(),
            epochs = epochs, callbacks = callbacks, validation_data = valid_generator,
            validation_steps = valid_generator.n_batches() if valid_generator is not None else None,
            max_q_size=max_q_size, workers=nb_worker, pickle_safe = True, class_weight = class_weights)

    if plot:
        plot_net(history)
    return history

def predict_generator(net, generator, output_cols, ids):
    y_pred = net.predict_generator(generator, steps = generator.n_batches(),
                            max_q_size = 10, workers=1, pickle_safe = True)
    df = pd.DataFrame(y_pred, columns = [str(x) for x in output_cols])
    return pd.concat((ids.reset_index(drop = True), df), axis = 1)

def load_net(file_name):
    return load_model(file_name)

def plot_net(history, save_to = None):
    from matplotlib import pyplot
    train_loss = history.history['loss']
    valid_loss = history.history['val_loss']
    pyplot.plot(train_loss, linewidth=3, label="train")
    pyplot.plot(valid_loss, linewidth=3, label="valid")
    pyplot.grid()
    pyplot.legend()
    pyplot.xlabel("epoch")
    pyplot.ylabel("loss")
    #pyplot.ylim(4e-1, 1)
    pyplot.yscale("log")
    try:
        if save_to:
            pyplot.savefig(save_to)
        else:
            pyplot.show()
    except RuntimeError as e:
        print "Unable to show plot", e

def get_balanced_class_weights(class_counts):
    return sum(class_counts) / (len(class_counts) * class_counts.astype(np.float32))
