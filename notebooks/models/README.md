## Models

Here you can see the steps taken to train and predict using each model.

The models present can be broken down into 3 categories.

First, we have **Simple models (supervised)**. These use the color histogram from the paintings, as well as the height/width ratio, to make predictions. On these, we generally used Bayesian optimization to find the best choices of hyperparameters. The same models were also applied to the principal components of our dataset. The models are:

- **Nearest Neighbors:** `KNN.ipynb`, `KNN_hist_sizes.ipynb`,
- **Naive Bayes:** `naive_bayes.ipynb`,
- **Logistic Regression:** `logistic_regression.ipynb`,
- **Support Vector Machines:** `SVM.ipynb`,
- **Decision Trees Ensembles:** `random_forest.ipynb`, `extra_tree.ipynb`, `gradient_boosting.ipynb`, `XGboost.ipynb`.

We also ran **K-means clustering** (`Kmeans.ipynb`).

Finally, based on the optimal hyperparameters for the previous models, and using as input, in addition to the color histograms and height/width ratio, the activations from the second to last layer of our neural network model (`nn_trained/net1`), we ran a **stacking classifier**, with a first layer containing all sorts of models, and a second layer with a random forest and an xgboost classifier, running on the cross validation predicted probabilities from all the different models in the first layer. The implementations can be found in `stack.ipynb`.