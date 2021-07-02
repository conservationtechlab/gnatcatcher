#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 19:25:10 2021

@author: amandabreton
"""

from microfaune.detection import RNNDetector
import scipy.io.wavfile
import os
import pandas as pd
import subprocess
from subprocess import call
import argparse
import yaml
import numpy as np
import exiftool
import matplotlib.pyplot as plt
# %%  yaml file example:
# csvpath = "/Users/amandabreton/Documents/GitHub/gnatcatcher/"
# path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
# analyzepath = '/Users/amandabreton/Documents/GitHub/BirdNET/analyze.py'
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

# %% using microfaune to filter audio files wtih events
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

# %% putting the info into a data frame
df = pd.DataFrame(list(zip(sounds, eventglobals, goodlocals)),
                  columns=['Audio_Paths', 'Highest_Event_Probability',
                           'Number_of_Events'])

# %% sending files to BirdNET analyze
os.chdir(birdnetpath)

for i in range(len(df['Audio_Paths'])):
    birdaud = str('python ') + str(analyzepath) + str(' --i ') + str(df['Audio_Paths'][i])
    subprocess.call(birdaud, shell=True)
    print('BirdNET done analyzing  audio file #' + str((i)))

print('BirdNET done analyzing ' + str(len(df['Audio_Paths']))
      + ' audio files')

# %% Most probable birds
files = os.listdir(path)  # Get all the files in that directory
txtfiles = []
for filename in os.listdir(path):
    if filename.endswith(".txt"):
        name = os.path.join(path, filename)
        txtfiles.append(name)
    else:
        nonimagecount = +1
        continue
# %%

knbirds = []
source = []
confidences = []
for k in range(len(txtfiles)):
    birdtxt = txtfiles[k]
    df = pd.read_csv(birdtxt, sep='\t')
    for i in range(1, len(df)):
        confid = df['Confidence'][i]
        confid = float(confid)
        if confid > threshold:
            # knbirds.append(confid)
            bird = df['Common Name'][i]
            knbirds.append(bird)
            audio = df['Begin File'][i]
            source.append(audio)
            confidences.append(confid)
        else:
            pass

df = pd.DataFrame(list(zip(knbirds, confidences, source)),
                  columns=['Species', 'Confidence', 'Audio Source'])

print('The most probable bird detections in this batch are as follows:')
print(df)

# %% graphing things
df1 = pd.DataFrame(list(zip(knbirds, source)),
                   columns=['Species', 'Audio Source'])
df1 = df1.groupby(df1.columns.tolist()).size().to_frame('Count').reset_index()

specieslist = []
[specieslist.append(x) for x in knbirds if x not in specieslist]

# %%
print('Here are the species found:')
print(specieslist)
print('Which species would you like to investigate further?')
bird = input()
# %%
sources = []
count = []
times = []
comments = []

for i in range(len(df1['Audio Source'])):
    if bird == str(df1['Species'][i]):
        audsource = (df1['Audio Source'][i])
        sources.append(audsource)
        freq = (df1['Count'][i])
        count.append(freq)
        exifpath = str(path) + str(df1['Audio Source'][i])
        with exiftool.ExifTool() as et:
            audComment = et.get_tag("comment", exifpath)
        time = audComment[13:20]
        comments.append(audComment)
        times.append(time)
    else:
        pass

df2 = pd.DataFrame(list(zip(times, sources, count)),
                   columns=['Time', 'Audio Source', 'Count'])
# %%
df2.plot.bar(x='Time', y='Count', rot=0)
plt.xlabel("Time")
plt.ylabel("Count")
plt.title(bird)
plt.show()
