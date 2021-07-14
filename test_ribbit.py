#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 12:14:23 2021

@author: amandabreton
"""
# suppress warnings
import warnings
warnings.simplefilter('ignore')

#import packages
import numpy as np
from glob import glob
import pandas as pd
from matplotlib import pyplot as plt
import argparse
import yaml

#local imports from opensoundscape
from opensoundscape.audio import Audio
from opensoundscape.spectrogram import Spectrogram
from opensoundscape.ribbit import ribbit
from opensoundscape.helpers import run_command

# create big visuals
plt.rcParams['figure.figsize'] = [15, 8]

# download files from box.com to the current directory
#_ = run_command(f"curl -L https://pitt.box.com/shared/static/9mrxib85y1jmf1ybbjvbr0tv171iekvy.gz -o ./great_plains_toad_dataset.tar.gz")# | tar -xz -f")
#_ = run_command(f"tar -xz -f great_plains_toad_dataset.tar.gz")

# this will print `0` if everything went correctly. If it prints 256 or another number, something is wrong (try downloading from the link above)

# using our own data: just put the audio into a folder w/ same name
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename

with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
audio_path = configs['path']
# audio_path is the path to a single audio file
# example:
# path: /Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/great_plains_toad_dataset/5D3C4530.WAV
# audio_path = np.sort(glob('./great_plains_toad_dataset/5D3C4530.WAV'))[0]
# load the audio file into an OpenSoundscape Audio object
audio = Audio.from_file(audio_path)

# trim the audio to the time from 0-3 seconds for a closer look
audio = audio.trim(0,3)
# create a Spectrogram object
spectrogram = Spectrogram.from_audio(audio)

#%%
spectrogram.plot()

# minimum and maximum rate of pulsing (pulses per second) to search for
pulse_rate_range = [10, 20]
# look for a vocalization in the range of 1000-2000 Hz
signal_band = [2000, 2500]
# subtract the amplitude signal from these frequency ranges
noise_bands = [ [0, 200], [10000, 10100]]
# divides the signal into segments this many seconds long, analyzes each independently
window_length = 2 #(seconds)
# if True, it will show the power spectrum plot for each audio segment
show_plots = True

# %% this is the part that gives you scoress
#get the audio file path
audio_path = np.sort(glob('./great_plains_toad_dataset/*'))[0]
#make the spectrogram
spec = Spectrogram.from_audio(audio.from_file(audio_path))

#run RIBBIT
scores, times =  ribbit(
                    spec,
                    pulse_rate_range=pulse_rate_range,
                    signal_band=signal_band,
                    window_len=window_length,
                    noise_bands=noise_bands,
                    plot=False)

#show the spectrogram
# print('spectrogram of 10 second file with Great Plains Toad at the beginning')
spec.plot()

# plot the score vs time of each window
plt.scatter(times,scores)
plt.xlabel('window start time (sec)')
plt.ylabel('RIBBIT score')
plt.title('RIBBIT scores for 10 second file with Great Plains Toad at the beginning')
print('The max score is:')
print(np.max(scores))
print('at time '+ str(np.max(times)) + ' sec')

# %%
#create a spectrogram from the file, like above:
# 1. get audio file path
audio_path = np.sort(glob('./great_plains_toad_dataset/'))[0]
# 2. make audio object and trim (this time 0-10 seconds)
audio = Audio.from_file(audio_path).trim(0,10)
# 3. make spectrogram
spectrogram = Spectrogram.from_audio(audio)

scores, times =  ribbit(
                        spectrogram,
                        pulse_rate_range=pulse_rate_range,
                        signal_band=signal_band,
                        window_len=window_length,
                        noise_bands=noise_bands,
                        plot=show_plots)

