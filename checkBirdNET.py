#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:19:38 2021

@author: amandabreton

Takes a more detailed look at a single output by BirdNET.
However you need to save the txt file created by BirdNET as
a csv file for this. If you would like a more efficient way
to look at the outputs created by BirdNET please run:
eventchecker.py with eventchecker.yaml followed by
eventplotter.py or eventplotter_all.py with eventchecker.yaml
"""
# %% import tools
import pyaudio
import wave
import pandas as pd
import time
import argparse
import yaml

# %% setup your files
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
audio = configs['audio']
datafile = configs['datafile']
threshold = configs['threshold']

# %% setting up a threshold in case one isn't provided
checker = isinstance(threshold, float)
if checker:
    threshold = threshold
else:
    threshold = 0.001

# %%
# setting up which sounds to hear

df = pd.read_csv(
    datafile, header=None)

knbirds = []
starts = []
ends = []
for i in range(1, len(df)):
    confid = df[10][i]
    confid = float(confid)
    if confid > threshold:
        # knbirds.append(confid)
        bird = df[9][i]
        knbirds.append(bird)
        begin = df[4][i]
        starts.append(begin)
        end = df[5][i]
        ends.append(end)
    else:
        pass

# %%  hearing the sounds

for i in range(len(knbirds)):
    File = audio
    print('Bird Guess is: ' + str(knbirds[i]))
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
    time.sleep(1)

print('There were ' + str(len(knbirds)) + ' bird call guesses total')
