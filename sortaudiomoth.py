#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 09:13:31 2021

@author: amandabreton
"""
import os 
import random 

path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
files = os.listdir(path)
sound = os.path.join(path, random.choice(files))

#%% doesn't work 
# https://pypi.org/project/wavinfo/ 

from wavinfo import WavInfoReader
info = WavInfoReader(sound)
#AttributeError: 'ListChunkDescriptor' object has no attribute 'ident'
#%% doesn't work 
# https://mutagen.readthedocs.io/en/latest/api/wave.html
import mutagen
audio = mutagen.File(sound)
audio.pprint()


#%% building up to bigger things 
import wave
#import numpy as np

file = wave.open(sound)
nchannels = file.getnchannels()
framerate = file.getframerate()
nframes = file.getnframes()

#%% 
import csv
import pandas
csvpath = "/Users/amandabreton/Documents/GitHub/brushdash/"

if os.path.exists(os.path.join(csvpath, "audiocsv.csv")):
  os.remove(os.path.join(csvpath, "audiocsv.csv"))
else:
  print("no audiocsv.csv file")
  
nonimagecount = 0
if os.path.exists(os.path.join(path, ".DS_Store")):
  os.remove(os.path.join(path, ".DS_Store"))
else:
  #print("no .DS_Store files")
  pass 
  
for filename in os.listdir(path):
    if filename.endswith(".wav"):
        name = os.path.join(path, filename)
    else:
        nonimagecount = +1
        continue  
   
sounds = [os.path.join(path, name) for name in os.listdir(path) if 
        os.path.isfile(os.path.join(path, name))]

length = len(sounds)
entrynum = list(range(0, length))
    
animals = ["bird", "dog", "cat", "lizard"]
classification = []
for k in range(length):
    fill = random.choice(animals)
    classification.append(fill)

#%%
f = open(os.path.join(csvpath, 'audiocsv.csv'), "a", newline = "")
writer = csv.writer(f)
writer.writerow(entrynum)
writer.writerow(sounds)
f.close()

data = pandas.read_csv(os.path.join(csvpath, 'imagecsv.csv'))
#print(data.describe())
data = data.transpose()
data.rename(columns={0: 'AudioPath', 1: 'Class'}, inplace=True)
data.to_csv(os.path.join(csvpath, 'imagecsv.csv'), index=False)
#data.ImagePath[2]