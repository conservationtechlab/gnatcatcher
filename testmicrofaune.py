#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 22:53:48 2021

@author: amandabreton
"""

from microfaune.detection import RNNDetector
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import scipy.io.wavfile
import contextlib
import wave

#path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
#files = os.listdir(path)
#sound = os.path.join(path, random.choice(files))
sound = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/5D3C4530.WAV'

detector = RNNDetector()
global_score, local_score = detector.predict_on_wav(sound)
fs, audData = scipy.io.wavfile.read(sound)

with contextlib.closing(wave.open(sound, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)

location = np.where(local_score == np.max(local_score))[0]
x = ((location*duration)/len(local_score))[0]
time = np.arange(0, duration, 1/fs)

plt.figure(1)
Pxx, freqs, bins, im = plt.specgram(audData, Fs=fs, NFFT=1024)
cbar = plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram of Entire Audio')
cbar.set_label('Intensity dB')
plt.axvspan(np.round(x), x, color='red', alpha=0.5)

# %%
print(global_score)
print(local_score)
print(len(local_score))
print(np.max(local_score))

print(location)
type(local_score)
plt.figure(2)
plt.plot(local_score)

# %%
plt.figure()
plt.plot(time, audData)
plt.axvspan(np.round(x), x, color='red', alpha=0.5)
plt.xlabel('Time (s)')
plt.ylabel('')

