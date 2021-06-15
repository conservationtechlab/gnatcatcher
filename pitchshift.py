#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os 
import random 
import sounddevice as sd
import soundfile as sf
import argparse 
import yaml
import contextlib
import wave
import matplotlib.pyplot as plt
import numpy as np

#parser = argparse.ArgumentParser()
#parser.add_argument('config_filename')
#args = parser.parse_args()
#CONFIG_FILE = args.config_filename
#with open(CONFIG_FILE) as f:
#    configs = yaml.load(f, Loader=yaml.SafeLoader)
#path = configs['path']
path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'

files = os.listdir(path)
sound = os.path.join(path, random.choice(files))
filename = sound

# Extract data and sampling rate from file
data, fs = sf.read(filename, dtype='float32')  

audlength = data.shape[0]/fs
with contextlib.closing(wave.open(sound,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print('The duration of sound is ' + str(duration) + ' seconds')

Pxx, freqs, bins, im = plt.specgram(data, Fs=fs, NFFT=1024)
maxF = max(freqs)
print('The maximum frequency is ' + str(maxF) + ' Hz')

if min(freqs) == 0.0:
    freqsnew = np.delete(freqs, (0), axis=0)
    
minF = min(freqsnew)
print('The minimum frequency is ' + str(minF) + ' Hz')
#%%
print('This sound is the original audio')
sd.play(data, fs)
status = sd.wait()  # Waits until file is done playing

print('This sound is the pitchshifted audio')
fs = fs/3
sd.play(data, fs)
status = sd.wait()

