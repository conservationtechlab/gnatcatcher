#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 16:00:24 2021

@author: amandabreton

Plays the guesses of where bird calls are at in an audio file using BirdNET.

Instructions:
    1. Have a csv file of the BirdNET selection
    2. Provide a configfile that includes:
        - the path to the folder containing the audio file
        - the path where the csv file of the audio is at
        Example of yaml file:
            audio = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/5D31ED38.WAV'
            datafile = '/Users/amandabreton/Documents/GitHub/gnatcatcher/BirdNet_csv_files/5D31ED38.BirdNET.csv'
    3. Run the code.
    It plays the parts of the audio where bird calls were detected
    It tells you:
        - the species of bird it thinks it is
        - time (sec) where the call is located
        - The confidence value in decimal
"""
import pyaudio
import wave
import pandas as pd
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

# %% sorting the vlaues - doesn't seem to be working
df = pd.read_csv(
    datafile, header=None)
temp = df.iloc[0]
df = df[1:]
df.columns = temp
df['time_0'] = df['Begin Time (s)'].apply(int)
df = df.sort_values(['time_0']).reset_index()

# %% creating the stuff to play
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

# %%  hearing the sounds

for i in range(len(knbirds)):
    File = audio
    print('Bird Guess is: ' + str(knbirds[i]))
    print('The time is from ' + str(starts[i]) + ' sec to ' + str(ends[i]) +
          ' sec')
    print('The confidence is ' + str(confids[i]))
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
