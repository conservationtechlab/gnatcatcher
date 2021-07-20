#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 20:44:11 2021

@author: amandabreton
"""

import os
import pandas as pd
from sklearn.metrics import average_precision_score
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
import matplotlib.pyplot as plt
# parse in paths to csvs and thresholds
testercsv = '/Users/amandabreton/Desktop/microfaune.csv'
grtruthcsv = '/Users/amandabreton/Desktop/groundtruth.csv'
threshold = 0.3

testerdf = pd.read_csv(testercsv, header=0)
grtruthdf = pd.read_csv(grtruthcsv,  header=0)

# %% firx the brackets on the testerdf
probabilities = []
for i in range(len(testerdf)):
    prob = testerdf['Probability'][i][1:-1]
    prob = float(prob)
    probabilities.append(prob)
# %% average precision score using the straight probabilities
# from microfaune
y_true = grtruthdf['Marker']
#y_true = y_true.to_numpy()
y_scores = probabilities
#y_scores = y_scores.to_numpy()
score = average_precision_score(y_true, y_scores)
print(score)
