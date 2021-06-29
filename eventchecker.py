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

# path where the soudns are hosted
# path where you want the csv file saved
csvpath = "/Users/amandabreton/Documents/GitHub/gnatcatcher/"
path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
threshold = 0.70

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

# %% work in progress - need to correctly parse in data
# but here is some psuedo code
# o = path where you want the BirdNET txt files saved
# i think will need to be in the same folder
# for i in range (len(df['Audio_Paths']))
#   i = df['Audio_Paths'][i]
#   import analyze.py //(from Birdnet)
#print('Done analyzing audio files.')
#import sys
#O = csvpath
#
#birdnetpath = '/Users/amandabreton/Documents/GitHub/BirdNET'
#for i in range (len(df['Audio_Paths'])):
#    I = df['Audio_Paths'][i]
#    sys.path.insert(0, birdnetpath)
#    import analyze
#print('Done analyzing audio files.')


# %%
import subprocess
from subprocess import call
import os
# %%
# subprocess.call(['python', 'somescript.py', somescript_arg1, somescript_val1,...])
birdinput = df['Audio_Paths'][3]
os.chdir("/Users/amandabreton/Documents/GitHub/BirdNET")
subprocess.call(['python', '/Users/amandabreton/Documents/GitHub/BirdNET/analyze.py', '--i /Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/20190726_033400.WAV'])

# %%
#from subprocess import Popen, PIPE

#p = Popen(['program', 'arg1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
#os.chmod("/Users/amandabreton/Documents/GitHub/BirdNET/analyze.py", 755)

#Popen(['/Users/amandabreton/Documents/GitHub/BirdNET/analyze.py', birdinput], stdin=PIPE, stdout=PIPE, stderr=PIPE)
