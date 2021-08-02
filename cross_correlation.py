#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 23:09:06 2021

@author: amandabreton
"""
# import modules
from scipy import signal
from scipy import misc
import numpy as np
import scipy.io.wavfile
from scipy.io import wavfile
import os
from os import walk
from glob import glob
import argparse
import yaml
# %% set up paths to mastlist of audio and unknown sample
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
ccpath = configs['ccpath']
unknbird = configs['unknbird']
# ccpath = '/Users/amandabreton/Documents/GitHub/gnatcatcher/cross_correlation_audio'
# unknbird = '/Users/amandabreton/Documents/GitHub/gnatcatcher/cross_correlation_audio/XC639456 - California Towhee - Melozone crissalis.wav'
# %% set up the audio you want to analyze
sample_rate, samples = wavfile.read(unknbird)
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
x, y = spectrogram.shape
start = round(.25*y)
end = round(.75*y)
segment = spectrogram[:, start:end]
# %% get list of paths to files and list of names
file_paths = glob(str(ccpath)+'/*.wav')
filenames = next(walk(ccpath), (None, None, []))[2]  # [] if no file
# %% for macOS, remove .DS_Store file
if os.path.exists(os.path.join(ccpath, ".DS_Store")):
    os.remove(os.path.join(ccpath, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

# %% perform cross correltation
maxcorrs = []
for i in range(len(file_paths)):
    knbird = file_paths[i]
    knbird_sr, knbird_samples = wavfile.read(knbird)
    frequencies, times, knspectrogram = signal.spectrogram(knbird_samples, knbird_sr)
    knsegment = knspectrogram
    corr = signal.correlate2d(segment, knsegment, boundary='symm', mode='same')
    maxcorr = np.max(corr)
    maxcorrs.append(maxcorr)

#%%
mostcorr = np.where(maxcorrs == np.max(maxcorrs))[0][0]
print('The closest species match is:')
print(filenames[mostcorr])
