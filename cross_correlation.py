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
import pandas as pd
import os
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

# %%  for mac os remove .DS_Store files
if os.path.exists(os.path.join(ccpath, ".DS_Store")):
    os.remove(os.path.join(ccpath, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

if os.path.exists(os.path.join(unknbirds, ".DS_Store")):
    os.remove(os.path.join(unknbirds, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass
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

# %% set up dataframe for later
times = np.arange(0,60,10)
#df = pd.DataFrame(index=unbirdsnames, columns=times)
df_corr = pd.DataFrame()
df_matches = pd.DataFrame()

# %%
matches = []
mostcorrs = []
confidences = []
for k in range(len(unbirds_paths)):
    unknbird = unbirds_paths[k]
    sample_rate, samples = wavfile.read(unknbird)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    truth = signal.correlate(spectrogram, spectrogram)
    maxcorrs = []
    for i in range(len(file_paths)):
        knbird = file_paths[i]
        knbird_sr, knbird_samples = wavfile.read(knbird)
        frequencies, times, knspectrogram = signal.spectrogram(knbird_samples, knbird_sr)
        #corr = signal.correlate2d(segment, knspectrogram, boundary='symm', mode='same')
        corr = signal.correlate(spectrogram, knspectrogram)
        maxcorr = np.max(corr)
        maxcorrs.append(maxcorr)
    mostcorr = np.where(maxcorrs == np.max(maxcorrs))[0][0]
    match = filenames[mostcorr]
    confidence = np.max(maxcorrs)/np.max(truth)
    confidences.append(confidence)
    matches.append(match)


# %%
df = pd.DataFrame(list(zip(unbirdsnames, matches, confidences)),
                  columns=['File Name', 'Closest Matched Species',
                           'Confidence Compared to Autocorrelation'])
df.to_csv(r'/Users/amandabreton/Desktop/testcc.csv')
