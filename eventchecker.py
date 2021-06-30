#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 19:25:10 2021

@author: amandabreton
"""

from microfaune.detection import RNNDetector
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile
import contextlib
import wave
import os
import pandas as pd
import subprocess
from subprocess import call
import argparse
import yaml
# %%
# path where the soudns are hosted
# path where you want the csv file saved
# csvpath = "/Users/amandabreton/Documents/GitHub/gnatcatcher/"
# path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
# birdnetpath = '/Users/amandabreton/Documents/GitHub/BirdNET/analyze.py'
# threshold = 0.70

# %% setup your files
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
csvpath = configs['csvpath']
path = configs['path']
birdnetpath = configs['birdnetpath']
threshold = configs['threshold']

# %%
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

# %%

eventlist = []
eventglobals = []
goodlocals = []
for i in range(len(sounds)):
    detector = RNNDetector()
    sound = sounds[i]
    global_score, local_score = detector.predict_on_wav(sound)
    s, audData = scipy.io.wavfile.read(sound)
    if global_score > threshold:
        eventlist.append(sound)
        eventglobals.append(global_score)
        count = len([k for k in local_score if k > threshold])
        goodlocals.append(count)
    else:
        pass

# %%
df = pd.DataFrame(list(zip(sounds, eventglobals, goodlocals)),
                  columns=['Audio_Paths', 'Highest_Event_Probability',
                           'Number_of_Events'])

# %%
os.chdir("/Users/amandabreton/Documents/GitHub/BirdNET")

for i in range(len(df['Audio_Paths'])):
    birdaud = str('python ') + str(birdnetpath) + str(' --i ') + str(df['Audio_Paths'][i])
    subprocess.call(birdaud, shell=True)
    print('BirdNET done analyzing  audio file #' + str((df['Audio_Paths'][i])))

print('BirdNET done analyzing ' + str(len(df['Audio_Paths']))
      + ' audio files')
