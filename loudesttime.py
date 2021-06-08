#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 12:33:57 2021

@author: amandabreton
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 00:38:59 2021

@author: amandabreton
"""
# I keep getting this error: 
# ValueError: File format b'\x00\x00\x00\x01' not understood. Only 'RIFF' and 'RIFX' supported.
# but if i just keep trying to run it, it's fine 
# it doesn't seem to work when run from the terminal though

#import libraries
import scipy.io.wavfile
import os 
import random 
import numpy as np
from numpy import fft as fft
import matplotlib.pyplot as plt
import argparse 
import yaml 
import wave
import contextlib
from scipy import fftpack as scfft
from scipy.fft import fft, ifft
# i do need this scipy.fft abs(fft(audData)) uses it 
from scipy.io.wavfile import write ,read
#import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename

with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
    
path = configs['path']
path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'

files = os.listdir(path)
sound = os.path.join(path, random.choice(files))

fs,audData=scipy.io.wavfile.read(sound)
print('sampling rate = ' +str(fs) + 'Hz')
audlength = audData.shape[0]/fs
#power - energy per unit of time
power = 1.0/(2*(audData.size)+1)*np.sum(audData.astype(float)**2)/fs

plt.figure(1, figsize=(8,6))
Pxx, freqs, bins, im = plt.specgram(audData, Fs=fs, NFFT=1024)
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram of Entire Audio')
cbar.set_label('Intensity dB')
# The `specgram` method returns 4 objects. They are:
# - Pxx: the periodogram
# - freqs: the frequency vector
# - bins: the centers of the time bins
# - im: the .image.AxesImage instance representing the data in the plot


with contextlib.closing(wave.open(sound,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print('Duration of sound:')
    print(duration)

#%% finding loudest part of the sound file 

avgpower = []
tempPxx = []
for i in range(len(bins)):
    tempPxx = Pxx[:, i:i+9]
    power = np.mean(tempPxx)
    avgpower.append(power)
    
#as of now this doesn't break it up into the chunks i want 
# but after this i think i can convert the power to decibels 
# so it's easier to see how the average loudness changes over time