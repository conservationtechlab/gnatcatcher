#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:19:38 2021

@author: amandabreton
"""
import pyaudio
import numpy as np
import wave
import struct
import pandas as pd
import time
audio = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/5D31ED38.WAV'
datafile = '/Users/amandabreton/Documents/GitHub/gnatcatcher/BirdNet csv Files/5D31ED38.BirdNET.csv'
threshold = 0.95
# %%
# setting up which sounds to hear

df = pd.read_csv(
    datafile, header=None)

knbirds = []
starts= []
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
    stream = py_audio.open(format=py_audio.get_format_from_width(wave_file.getsampwidth()),
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

print('There were ' + str(len(knbirds)) + ' bird call guesses total')
