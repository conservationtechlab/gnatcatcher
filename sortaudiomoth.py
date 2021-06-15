#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 09:13:31 2021

@author: amandabreton
"""
import os 
import random 
import csv
import pandas
import wave

csvpath = "/Users/amandabreton/Documents/GitHub/gnatcatcher/"

#%% doesn't work 
# https://pypi.org/project/wavinfo/ 
path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
files = os.listdir(path)
sound = os.path.join(path, random.choice(files))

from wavinfo import WavInfoReader
info = WavInfoReader(sound)
#AttributeError: 'ListChunkDescriptor' object has no attribute 'ident'
#%% doesn't work 
# https://mutagen.readthedocs.io/en/latest/api/wave.html
import mutagen
audio = mutagen.File(sound)
audio.pprint()


#%% extracting data in a simpler but longer way 

if os.path.exists(os.path.join(csvpath, "audiocsv.csv")):
  os.remove(os.path.join(csvpath, "audiocsv.csv"))
else:
  #print("no audiocsv.csv file")
  pass

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
    
channelarray = []
samplerates = []
framenums = []
for k in range(length):
    sample = sounds[k]
    file = wave.open(sample)
    nchannel = file.getnchannels()
    channelarray.append(nchannel)
    fs = file.getframerate()
    samplerates.append(fs)
    frames = file.getnframes()
    framenums.append(frames)
    
f = open(os.path.join(csvpath, 'audiocsv.csv'), "a", newline = "")
writer = csv.writer(f)
writer.writerow(entrynum)
writer.writerow(sounds)
writer.writerow(channelarray)
writer.writerow(samplerates)
writer.writerow(framenums)
f.close()

data = pandas.read_csv(os.path.join(csvpath, 'audiocsv.csv'))
data = data.transpose()
data.rename(columns={0: 'AudioPath', 1: 'Channels', 2: 'Sample Rate (Hz)', 3: 'Number of Frames'}, inplace=True)
data.to_csv(os.path.join(csvpath, 'audiocsv.csv'), index=False)
