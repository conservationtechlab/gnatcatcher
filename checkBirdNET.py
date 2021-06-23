#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:19:38 2021

@author: amandabreton
"""
import pyaudio
# import sys
import numpy as np
import wave
import struct
import pandas as pd
import time

audio = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/5D31ED38.WAV'
data = '/Users/amandabreton/Documents/GitHub/gnatcatcher/BirdNet csv Files/5D31ED38.BirdNET.csv'
threshold = 0.95
# %%
# setting up which sounds to hear

df = pd.read_csv(
    data, header=None)

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
File = audio

for i in range(len(knbirds)):
    print('Bird Guess is: ' + str(knbirds[i]))
    print('The time is from ' + str(starts[i]) + ' sec to ' + str(ends[i]))
    start = int(starts[i])
    stop = int(ends[i])
    length = int(ends[i]) - int(starts[i])
    chunk = 1024

    spf = wave.open(File, 'rb')
    signal = spf.readframes(-1)
    # signal = np.fromstring(signal, 'Int16')
    signal = np.frombuffer(signal, 'Int16')
    p = pyaudio.PyAudio()

    stream = p.open(format=
                    p.get_format_from_width(spf.getsampwidth()),
                    channels=spf.getnchannels(),
                    rate=spf.getframerate(),
                    output=True)

    pos = spf.getframerate()*length
    signal = signal[start*spf.getframerate():(start*spf.getframerate()) + pos]
    sig = signal[1:chunk]

    inc = 0
    data = 0

    # play
    while data != '':
        data = struct.pack("%dh" % (len(sig)), *list(sig))
        stream.write(data)
        inc = inc+chunk
        sig = signal[inc:inc+chunk]

    # stream.close()
    # p.terminate()
    time.sleep(2)
