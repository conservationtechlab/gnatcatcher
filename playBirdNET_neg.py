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
import argparse
import yaml

def ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))


# %% setup your files
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
audio = configs['audio']
datafile = configs['datafile']

# %% getting duration
with contextlib.closing(wave.open(audio, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)

timestep = np.arange(0, duration+1)

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

# %%
negsrange = ranges(negs)
starts = []
ends = []
for i in range(len(negsrange)):
    s = negsrange[i][0]
    starts.append(s)
    e = negsrange[i][1]
    ends.append(e)

# %%  hearing where there is supposedly no birds
if (len(negsrange) == 1):
    print('There are no silent times in this audio sample')
else:
    for i in range(len(starts)):
        File = audio
        print('There should be no bird calls here.')
        print('The time is from ' + str(starts[i]) + ' sec to ' + str(ends[i]) +
              ' sec')
    # set desired values
        start = int(starts[i])
        stop = int(ends[i])
        length = stop - start

        # open wave file
        wave_file = wave.open(audio, 'rb')

        # initialize audio
        py_audio = pyaudio.PyAudio()
        stream = py_audio.open(
            format=py_audio.get_format_from_width(wave_file.getsampwidth()),
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True)

        # skip unwanted frames
        n_frames = int(start * wave_file.getframerate())
        wave_file.setpos(n_frames)

        # write desired frames to audio buffer
        n_frames = int(length * wave_file.getframerate())
        frames = wave_file.readframes(n_frames)
        stream.write(frames)

        # close and terminate everything properly
        stream.close()
        py_audio.terminate()
        wave_file.close()
