#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 22:53:48 2021

@author: amandabreton

A script used for testing the robustness of microfaune.
It outputs a csv file containing the results from microfaune.
"""

from microfaune.detection import RNNDetector
import scipy.io.wavfile
import os
from os import walk
import pandas as pd
import subprocess
from subprocess import call
import argparse
import yaml
import numpy as np
import exiftool
import matplotlib.pyplot as plt

# %%  yaml file example:
# csvpath:"/Users/amandabreton/Documents/GitHub/gnatcatcher/"
# path: '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
# analyzepath: '/Users/amandabreton/Documents/GitHub/BirdNET/analyze.py'
# threshold: 0.70

# %% setup your files
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
   configs = yaml.load(f, Loader=yaml.SafeLoader)
csvpath = configs['csvpath']
path = configs['path']
analyzepath = configs['analyzepath']
birdnetpath = configs['birdnetpath']
threshold = configs['threshold']

# %% getting which files are audio
if os.path.exists(os.path.join(csvpath, "eventlist.csv")):
    os.remove(os.path.join(csvpath, "eventlist.csv"))
else:
    # print("no audiocsv.csv file")
    pass

nonimagecount = 0
if os.path.exists(os.path.join(path, ".DS_Store")):
    os.remove(os.path.join(path, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

for filename in os.listdir(path):
    if filename.endswith(".wav"):
        name = os.path.join(path, filename)
    else:
        nonimagecount = +1
        continue

sounds = [os.path.join(path, name) for name in os.listdir(path) if
          os.path.isfile(os.path.join(path, name))]

audnames = next(walk(path), (None, None, []))[2]
# %% using microfaune to filter audio files wtih events
eventlist = []
eventglobals = []
goodlocals = []
for i in range(len(sounds)):
    detector = RNNDetector()
    sound = sounds[i]
    global_score, local_score = detector.predict_on_wav(sound)
    s, audData = scipy.io.wavfile.read(sound)
    eventlist.append(sound)
    eventglobals.append(global_score)


# %% putting the info into a data frame
df = pd.DataFrame(list(zip(audnames, eventglobals)),
                  columns=['Audio', 'Probability'])
df.to_csv('SONGBIRDSmicrofaune.csv')
