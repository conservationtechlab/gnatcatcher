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
import urllib
import scipy.io.wavfile
import pydub
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
import pandas
#import seaborn as sns

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

#Fourier Transform 
fs, audData  = read(sound)
l_audio = len(audData.shape)
N = audData.shape[0]
secs = N / float(fs)
Ts = 1.0/fs
t = np.arange(0, secs, Ts) 
FFT = abs(fft(audData))
FFT_side = FFT[range(N//2)] 
freqs = scipy.fftpack.fftfreq(audData.size, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N//2)] 
fft_freqs_side = np.array(freqs_side)

volume=np.array(abs(FFT_side))
audible=np.where(volume>5)
HighestAudibleFrequency=max(freqs_side[audible])
print('Highest Audible Frequency = ' + str(HighestAudibleFrequency) + 'Hz')

plt.figure(2, figsize=(8,6))
plt.plot(FFT)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.title('Fast Fourier Transform of Entire Audio')

with contextlib.closing(wave.open(sound,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print('Duration of sound:')
    print(duration)

# choosing a specific part to analyze    
t0 = int(input("Enter start time "))
tf = int(input("Enter end time "))
f0 = t0*rate
ff = tf*rate

segment = audData[f0:ff]
plt.figure(3, figsize=(8,6))
Pxx, freqs, bins, im = plt.specgram(segment, Fs=fs, NFFT=1024)
# The `specgram` method returns 4 objects. They are:
# - Pxx: the periodogram
# - freqs: the frequency vector
# - bins: the centers of the time bins
# - im: the .image.AxesImage instance representing the data in the plot
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram of Segmented Time')
cbar.set_label('Intensity dB')

row, col = np.where(Pxx == np.max(Pxx))
intensF = freqs[row][0]

if intensF == 0.0:
    Pxxnew = np.delete(Pxx, (0), axis=0)
    freqsnew = np.delete(freqs, (0), axis=0)
    row, col = np.where(Pxx == np.max(Pxx))
    intensF = freqsnew[row][0]
    
print('The most prominent frequency = ' + str(intensF) + ' Hz')

#%% plotting the strongest frequencies over the time frame 
    
plt.figure(4, figsize=(8,6))
Pxx, freqs, bins, im = plt.specgram(audData, Fs=fs, NFFT=1024)
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram of Entire Audio')
cbar.set_label('Intensity dB')

rows, cols = Pxx.shape
maxpower = []
maxfreqs = []
for i in range(cols):
    power = np.max(Pxx[:,i])
    maxpower.append(power)
    val = np.argmax(Pxx[:,i])
    maxfreqs.append(val)
 
plt.figure(5, figsize=(8,6))
plt.subplot(211)
plt.plot(maxfreqs)  
plt.xlabel('bin number')
plt.ylabel('Frequency (Hz)')
plt.title('Strongest Frequency per bin')
plt.subplot(212)
plt.plot(maxpower)  
plt.xlabel('bin number')
plt.ylabel('Power')
plt.title('Power of Strongest Frequency per Bin')
# need to figure it out per time frame rather than bin 
# the whale sound data is not a great example because it's FFT is so weird
# it thinks the strongest freqency is 