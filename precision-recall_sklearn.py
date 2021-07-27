#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 20:44:11 2021

@author: amandabreton
"""

import pandas as pd
from sklearn.metrics import average_precision_score
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
import matplotlib.pyplot as plt
from sklearn.metrics import average_precision_score
import argparse
import yaml

# parse in paths to csvs and thresholds
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
testercsv = configs['testercsv']
grtruthcsv = configs['grtruthcsv']

# example:
# testercsv: /Users/amandabreton/Desktop/microfaune.csv
# grtruthcsv :/Users/amandabreton/Desktop/groundtruth.csv

# testercsv = '/Users/amandabreton/Desktop/microfaune.csv'
# grtruthcsv = '/Users/amandabreton/Desktop/groundtruth.csv'

testerdf = pd.read_csv(testercsv, header=0)
grtruthdf = pd.read_csv(grtruthcsv,  header=0)

# %% fix the brackets on the testerdf
probabilities = []
for i in range(len(testerdf)):
    prob = testerdf['Probability'][i][1:-1]
    prob = float(prob)
    probabilities.append(prob)

# %% set up numpy.ndarray for graphing
y = grtruthdf['Marker']
y = np.array(y)
X = probabilities
X = np.array(probabilities)
X = X.reshape(-1, 1)
random_state = np.random.RandomState(0)

# Create a simple classifier
classifier = svm.LinearSVC(random_state=random_state)
classifier.fit(X, y)
y_score = classifier.decision_function(X)

average_precision = average_precision_score(y, y_score)

print('Average precision-recall score: {0:0.2f}'.format(
      average_precision))

disp = plot_precision_recall_curve(classifier, X, y)
disp.ax_.set_title('2-class Precision-Recall curve: '
                   'AP={0:0.2f}'.format(average_precision))


# %%
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc

#y = label_binarize(y, classes=[0, 1])
#n_classes = y.shape[1]

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()

fpr, tpr, _ = roc_curve(y, y_score)
roc_auc = auc(fpr, tpr)

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)

plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve (Receiver Operating Characteristic)')
plt.legend(loc="lower right")
plt.show()
