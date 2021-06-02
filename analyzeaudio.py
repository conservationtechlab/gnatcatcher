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
#print('audio wave data = '),print(audData)
audlength = audData.shape[0]/fs

#power - energy per unit of time
power = 1.0/(2*(audData.size)+1)*np.sum(audData.astype(float)**2)/fs

#fourier=fft.fft(audData)
#plt.plot(fourier, color='#ff7f00')
#plt.xlabel('k')
#plt.ylabel('Amplitude')
# this also gives us the imaginary stuff which we don't 
# really want to see right now 
#n = len(audData)
#fourier = fourier[0:(n/2)]
# getting error below so going to ignore this for now 
#^ TypeError: slice indices must be integers or None or have an __index__ method
# scale by the number of points so that the magnitude does not depend on the length
#fourier = fourier/float(n)

#calculate the frequency at each point in Hz
#freqArray = np.arange(0, (n/2), 1.0) * (rate*1.0/n);

#plt.plot(freqArray/1000, 10*np.log10(fourier), color='#ff7f00', linewidth=0.02)
#plt.xlabel('Frequency (kHz)')
#plt.ylabel('Power (dB)')

plt.figure(1, figsize=(8,6))
Pxx, freqs, bins, im = plt.specgram(audData, Fs=fs, NFFT=1024)
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram')
cbar.set_label('Intensity dB')

# this doesn't work: 
#where  = np.where(freqs==2000)
#MHZ10=Pxx[where,:]
#plt.plot(bins, MHZ10, color='#ff7f00')
#plt.show()
# need to employ a counter for the freqs i think
# or some sort of histogram

#%% 
# psuedocode
# need to split the time frame up: 
#    
t0 = int(input("Enter start time "))
tf = int(input("Enter end time "))
segment = audData[t0:tf]
plt.figure(2, figsize=(8,6))
Pxx, freqs, bins, im = plt.specgram(segment, Fs=fs, NFFT=1024)
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram of Segmented Time')
cbar.set_label('Intensity dB')
plt.figure(2, figsize=(8,6))
plt.hist(freqs)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Counts')
plt.title('Histogram')


#%% New stuff on Fourier Transform 
from scipy import fftpack as scfft
from scipy.fft import fft, ifft
from scipy.io.wavfile import write ,read

fs, audData  = read(sound)
l_audio = len(audData.shape)
N = audData.shape[0]
secs = N / float(fs)
Ts = 1.0/fs
#t = scipy.arange(0, secs, Ts) 
# "scipy.arange is deprecated and will be removed in SciPy 2.0.0, use numpy.arange instead"
t = np.arange(0, secs, Ts) 
#FFT = abs(scipy.fft(audData))
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

plt.figure(3, figsize=(8,6))
plt.plot(FFT)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power')
plt.title('Fast Fourier Transform')

#next step: getting a histogram of all the frequency values
