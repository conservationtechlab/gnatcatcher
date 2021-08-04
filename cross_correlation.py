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
# parser = argparse.ArgumentParser()
# parser.add_argument('config_filename')
# args = parser.parse_args()
# CONFIG_FILE = args.config_filename
# with open(CONFIG_FILE) as f:
#     configs = yaml.load(f, Loader=yaml.SafeLoader)
# ccpath = configs['ccpath']
# unknbird = configs['unknbird']
# %%
ccpath = '/Users/amandabreton/Documents/GitHub/gnatcatcher/cross_correlation_audio'
unknbirds = '/Users/amandabreton/Documents/GitHub/gnatcatcher/cross_correlation_audio/UnknownBirds'

# %% get list of paths to masterlist files and list of names in the masterlist
file_paths = glob(str(ccpath)+'/*.wav')
filenames = next(walk(ccpath), (None, None, []))[2]  # [] if no file

# %%
unbirds_paths = glob(str(unknbirds)+'/*.wav')
unbirdsnames = next(walk(unknbirds), (None, None, []))[2]  # [] if no file

# %% for macOS, remove .DS_Store file
if os.path.exists(os.path.join(ccpath, ".DS_Store")):
    os.remove(os.path.join(ccpath, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

# %% set up strings for dataframe for later
matches = []
# %% for loop 
   # set up the audio you want to analyze
for k in range(len(unbirds_paths)):
    unknbird = unbirds_paths[k]
    sample_rate, samples = wavfile.read(unknbird)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    x, y = spectrogram.shape
    timesegs = np.linspace(0, y, num=7)
    timesegs = np.round(timesegs)
    timesegs = timesegs.astype(int)
    for j in range(len(timesegs)-1):
        segment = spectrogram[:, timesegs[j]:timesegs[j+1]]
        maxcorrs = []
    # perform cross correltation
        for i in range(len(file_paths)):
            knbird = file_paths[i]
            knbird_sr, knbird_samples = wavfile.read(knbird)
            frequencies, times, knspectrogram = signal.spectrogram(knbird_samples, knbird_sr)
            x, y = knspectrogram.shape
            start = round(.25*y)
            end = round(.75*y)
            knsegment = knspectrogram[:, start:end]
            #corr = signal.correlate2d(segment, knsegment, boundary='symm', mode='same')
            corr = signal.correlate(segment, knsegment)
            maxcorr = np.max(corr)
            maxcorrs.append(maxcorr)
            mostcorr = np.where(maxcorrs == np.max(maxcorrs))[0][0]
            match = filenames[mostcorr]
        matches.append(match)


