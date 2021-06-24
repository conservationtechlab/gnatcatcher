#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 22:19:40 2021

@author: amandabreton
"""

import pyaudio
import wave
import pandas as pd
import os
import contextlib
import numpy as np
audio = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/5D3C4530.WAV'
datafile = '/Users/amandabreton/Documents/GitHub/gnatcatcher/BirdNet_csv_files/5D3C4530.BirdNET.csv'

# %% getting duration

with contextlib.closing(wave.open(audio, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)

timestep = np.arange(0,duration+1)

# %% 
df = pd.read_csv(
    datafile, header=None)
temp = df.iloc[0]
df = df[1:]
df.columns = temp
df['time_0'] = df['Begin Time (s)'].apply(int)
df = df.sort_values(['time_0']).reset_index()

# %% creating the stuff NOT to play
knbirds = []
starts = []
ends = []
confids = []
for i in range(len(df['time_0'])):
    bird = df['Common Name'][i]
    knbirds.append(bird)
    begin = df['Begin Time (s)'][i]
    starts.append(begin)
    end = df['End Time (s)'][i]
    ends.append(end)
    confid = df['Confidence'][i]
    confids.append(confid)
else:
    pass

stored = []
for i in range(len(knbirds)):
    boi = np.arange(int(starts[i]), int(ends[i]))
    stored.append(boi)
    
stored = np.transpose(stored)
row, col = stored.shape

whole = []
for i in range(row):
    for k in range(col):
        new = stored[i][k]
        whole.append(new)

whole = np.array(whole)
# %%

negs = []
for i in range(len(timestep)):
    val = timestep[i]
    if val in whole:
        pass
    else:
        negs.append(val)
negs = np.array(negs)