#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:50:06 2021

@author: amandabreton

A python code used to test out Opensoundscape's RIBBIT.
You don't need to parse anything in, it's supposed to be
set to the great_plains_toad_dataset provided by Opensoundscape.
"""

# suppress warnings
import warnings
warnings.simplefilter('ignore')
# import packages
import numpy as np
from glob import glob
import pandas as pd
from matplotlib import pyplot as plt
# local imports from opensoundscape
from opensoundscape.audio import Audio
from opensoundscape.spectrogram import Spectrogram
from opensoundscape.ribbit import ribbit
from opensoundscape.helpers import run_command

# 55 set up the audio you want
audio_path = np.sort(glob('./great_plains_toad_dataset/'))[0]

# %%
# create big visuals
plt.rcParams['figure.figsize'] = [15, 8]

# using our own data: just put the audio into a folder w/ same name
# load the audio file into an OpenSoundscape Audio object
audio = Audio.from_file(audio_path)

# trim the audio to the time from 0-3 seconds for a closer look
audio = audio.trim(0, 3)
# create a Spectrogram object
spectrogram = Spectrogram.from_audio(audio)
spectrogram.plot()

# minimum and maximum rate of pulsing (pulses per second) to search for
pulse_rate_range = [10, 20]
# look for a vocalization in the range of 1000-2000 Hz
signal_band = [2000, 2500]
# subtract the amplitude signal from these frequency ranges
noise_bands = [[0, 200], [10000, 10100]]
# divides the signal into segments this many seconds long
# analyzes each independently
window_length = 2  # (seconds)
# if True, it will show the power spectrum plot for each audio segment
show_plots = True

# scoring
spec = Spectrogram.from_audio(audio.from_file(audio_path))
# run RIBBIT
scores, times = ribbit(
                    spec,
                    pulse_rate_range=pulse_rate_range,
                    signal_band=signal_band,
                    window_len=window_length,
                    noise_bands=noise_bands,
                    plot=False)

# plot the score vs time of each window
plt.scatter(times, scores)
plt.xlabel('window start time (sec)')
plt.ylabel('RIBBIT score')
plt.title('RIBBIT Scores')
print('The max score is:')
print(np.max(scores))
print('at time ' + str(np.max(times)) + ' sec')
