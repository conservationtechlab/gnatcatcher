#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 09:13:31 2021
@author: amandabreton

Provides a summary of the audio data in a given folder.

Instructions:
    1. Install PyExifTool using "pip install PyExifTool"
    2. Provide a configfile that includes:
        - the path to the folder containing the audio files
        - the path where you want the csv file to be saved
        Example of yaml file:
            csvpath = "/Users/amandabreton/Documents/GitHub/gnatcatcher/"
            path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
    3. Run the code. It should provide a csv file containing:
        Path of the audio file, # of channels, sample rate, # of frames ,
        time (sec), most prominent frequency (mpf), loudness of mpf,
        time of mpf, average loudness, any comments found in audio's metadata'
"""
import os
import random
import csv
import pandas
import wave
import matplotlib.pyplot as plt
import scipy
import contextlib
import numpy as np
import math
import argparse
import yaml
import exiftool
import scipy.io.wavfile

parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
path = configs['path']
csvpath = configs['csvpath']

files = os.listdir(path)

# %%
# extracting data in a simpler but longer way

if os.path.exists(os.path.join(csvpath, "audiocsv.csv")):
    os.remove(os.path.join(csvpath, "audiocsv.csv"))
else:
    # print("no audiocsv.csv file")
    pass

nonimagecount = 0
if os.path.exists(os.path.join(path, ".DS_Store")):
    os.remove(os.path.join(path, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

for filename in os.listdir(path):
    if filename.endswith(".wav"):
        name = os.path.join(path, filename)
    else:
        nonimagecount = +1
        continue

sounds = [os.path.join(path, name) for name in os.listdir(path) if
          os.path.isfile(os.path.join(path, name))]

length = len(sounds)
entrynum = list(range(0, length))

channelarray = []
samplerates = []
framenums = []
durationarray = []
IFarray = []
loudness = []
loudtime = []
avgloudness = []
comments = []

for k in range(length):
    sample = sounds[k]
    file = wave.open(sample)
    nchannel = file.getnchannels()
    channelarray.append(nchannel)
    fs = file.getframerate()
    samplerates.append(fs)
    frames = file.getnframes()
    framenums.append(frames)
    fs, audData = scipy.io.wavfile.read(sample)
    #Pxx, freqs, bins, im = plt.specgram(audData, Fs=fs, NFFT=1024)
    with contextlib.closing(wave.open(sample, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    durationarray.append(duration)
    #row, col = np.where(Pxx == np.max(Pxx))
    #intensF = freqs[row][0]
    #if intensF == 0.0:
    #    Pxxnew = np.delete(Pxx, (0), axis=0)
    #    freqsnew = np.delete(freqs, (0), axis=0)
    #    row, col = np.where(Pxx == np.max(Pxx))
    #   intensF = freqsnew[row][0]
    #IFarray.append(intensF)
    #dec = math.log(np.max(Pxx))
    # double check the math for calculating decibels
    #loudness.append(dec)
    #x = ((col*duration)/len(bins))[0]
    #loudtime.append(x)
    #avgL = math.log(np.mean(Pxx))
    #avgloudness.append(avgL)
    with exiftool.ExifTool() as et:
        audComment = et.get_tag("comment", sample)
    comments.append(audComment)

f = open(os.path.join(csvpath, 'audiocsv.csv'), "a", newline="")
writer = csv.writer(f)
writer.writerow(entrynum)
writer.writerow(sounds)
writer.writerow(channelarray)
writer.writerow(samplerates)
writer.writerow(framenums)
writer.writerow(durationarray)
writer.writerow(IFarray)
writer.writerow(loudness)
writer.writerow(loudtime)
writer.writerow(avgloudness)
writer.writerow(comments)
f.close()

data = pandas.read_csv(os.path.join(csvpath, 'audiocsv.csv'))
data = data.transpose()
data.rename(columns={0: 'AudioPath', 1: 'Channels',
                     2: 'Sample Rate (Hz)', 3: 'Number of Frames',
                     4: 'Time (sec)', 5: 'Most Prominent Frequency (MPF)',
                     6: 'Loudness of MPF (dB)', 7: 'Time of Loudest Freq',
                     8: 'Average Loudness (dB)', 9: 'Comments'}, inplace=True)
data.to_csv(os.path.join(csvpath, 'audiocsv.csv'), index=False)
