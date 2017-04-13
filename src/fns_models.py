import pandas as pd
import numpy as np
import os
import re
import random
from matplotlib import pyplot as plt
from PIL import Image

# Pick top 3 authors
def get_top_author(num_author=3):
    train = pd.read_csv("data/train_hist_author_knn.csv")
    test = pd.read_csv("data/test_hist_author_knn.csv")

    print "[INFO] The size of train histogram for Random Forest" + str(train.shape)
    print "[INFO] The size of test histogram for Random Forest" + str(test.shape)

     
    train.iloc[:,2:-3] = train.iloc[:, 2:-3]\
        .apply(lambda x: x.astype(np.float) / (x.sum()/3), axis = 1, raw = True)
    test.iloc[:,2:-3] = test.iloc[:, 2:-3]\
        .apply(lambda x: x.astype(np.float) / (x.sum()/3), axis = 1, raw = True)
        
    author_index = train.author_id.value_counts().index[:num_author]
    train = train.loc[train['author_id'].isin(author_index)]
    test = test.loc[test['author_id'].isin(author_index)]
    
    
    print train.author_id.value_counts().head(10)
    print "[trian above] " + '=' * 50 + "[test below]"
    print test.author_id.value_counts().head(10)
    

    train_labels = train.author_id
    print train_labels.shape
    print  train.shape
    train = train.drop(['author_id', 'painting_id', 'height_px', 'width_px'], axis=1)
    test_labels = test.author_id
    test = test.drop(['author_id', 'painting_id', 'height_px', 'width_px'], axis=1)
   
    return train, train_labels, test, test_labels

# train, train_labels, test, test_labels = get_top_author(3)

def get_top_movement(num_movements = 3):
    movement_hist_train = pd.read_csv('data/movement_hist_train.csv')
    movement_hist_test = pd.read_csv('data/movement_hist_test.csv')
    
    print "[INFO] The size of train histogram for Random Forest" + str(movement_hist_train.shape)
    print "[INFO] The size of test histogram for Random Forest" + str(movement_hist_test.shape)

    movement_hist_train.iloc[:,3:-1] = movement_hist_train.iloc[:, 3:-1]\
        .apply(lambda x: x.astype(np.float) / (x.sum()/3), axis = 1, raw = True)

    movement_hist_test.iloc[:,3:-1] = movement_hist_test.iloc[:, 3:-1]\
            .apply(lambda x: x.astype(np.float) / (x.sum()/3), axis = 1, raw = True)
    
    mv_index = movement_hist_train['sup_art_movement'].value_counts().index[:num_movements]
    train = movement_hist_train[movement_hist_train['sup_art_movement'].isin(mv_index)]
    test = movement_hist_test[movement_hist_test['sup_art_movement'].isin(mv_index)]
    
    train_label = train['sup_art_movement']
    test_label = test['sup_art_movement']
    
    print 'top movement for train:\n %s ' % str(train['sup_art_movement'].value_counts())
    print '-' * 50
    print 'top movement for test:\n %s ' % str(test['sup_art_movement'].value_counts())

    test = test.drop(['author_id', 'painting_id', 'sup_art_movement'], axis=1)
    train = train.drop(['author_id', 'painting_id', 'sup_art_movement'], axis=1)

    return train, train_label, test, test_label

# train, train_label, test, test_label = get_top_movement(3)

def movement_encod(train_labels, test_labels):
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()
    le.fit(train_labels)
    le.classes_
    train_labels_encd = le.transform(train_labels)
    test_labels_encd = le.transform(test_labels)
    
    print "[INFO] the original train labels: %s" % str(train_labels.unique())
    print "[INFO] the encoded labels: %s" % str(train_labels_encd)
    
    print '-' * 50
    print "[INFO] the original train labels: %s" % str(test_labels.unique())
    print "[INFO] the encoded labels: %s" % str(test_labels_encd)
    
    return train_labels_encd, test_labels_encd


    
def result_table(y_true, y_pred):
    rslt = y_true  == y_pred

    test_data_df = pd.DataFrame()
    test_data_df.insert(0,'actual',y_true)
    test_data_df.insert(1,'predictions',y_pred)
    test_data_df.insert(2,'results',rslt)
    
    return test_data_df


def plot_columns(sample_painting):
    if len(sample_painting) > 8:
        sample_painting = sample_painting.sample(8)

    size = len(sample_painting)
    y = 1 if size <= 4 else 2
    x = size if y == 1 else (size + 1) // 2
    f, ax = plt.subplots(y, x, figsize = (20,15))
    for i in range(size):
        im = Image.open('data/images_athenaeum/full/%d/%d.jpg' % (sample_painting.iloc[i]['author_id'],
                                                                  sample_painting.iloc[i]['painting_id']))
        if size == 1:
            ax.imshow(im)
        elif y == 1:
            ax[i].imshow(im)
        else:
            ax[i / x, i % x].imshow(im)











# get data for all 
# def get_data():
#     train = pd.read_csv("data/train_hist_author_knn.csv")
#     test = pd.read_csv("data/test_hist_author_knn.csv")

#     print "[INFO] The size of train histogram for Random Forest" + str(train.shape)
#     print "[INFO] The size of test histogram for Random Forest" + str(test.shape)

#     train_labels = train.author_id
#     train = train.drop(['author_id', 'painting_id'], axis=1)
#     test_labels = test.author_id
#     test = test.drop(['author_id', 'painting_id'], axis=1)
    
#     train.iloc[:,:-2] = train.iloc[:, :-2]\
#         .apply(lambda x: x.astype(np.float) / (x.sum()/3), axis = 1, raw = True)
#     test.iloc[:,:-2] = test.iloc[:, :-2]\
#         .apply(lambda x: x.astype(np.float) / (x.sum()/3), axis = 1, raw = True)
    
#     return train, train_labels, test, test_labels

# train, train_labels, test, test_labels = get_data()
