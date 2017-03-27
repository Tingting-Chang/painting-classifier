import pandas as pd
import numpy as np
import os
import re
import random


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

def result_table(y_true, y_pred):
    rslt = y_true  == y_pred

    test_data_df = pd.DataFrame()
    test_data_df.insert(0,'actual',y_true)
    test_data_df.insert(1,'predictions',y_pred)
    test_data_df.insert(2,'results',rslt)
    
    return test_data_df


def plot_bo(f, bo):
    xs = [x["x"] for x in bo.res["all"]["params"]]
    ys = bo.res["all"]["values"]

    mean, sigma = bo.gp.predict(np.arange(len(f)).reshape(-1, 1), return_std=True)
    
    plt.figure(figsize=(16, 9))
    plt.plot(f)
    plt.plot(np.arange(len(f)), mean)
    plt.fill_between(np.arange(len(f)), mean+sigma, mean-sigma, alpha=0.1)
    plt.scatter(bo.X.flatten(), bo.Y, c="red", s=50, zorder=10)
    plt.xlim(0, len(f))
    plt.ylim(f.min()-0.1*(f.max()-f.min()), f.max()+0.1*(f.max()-f.min()))
    plt.show()













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
