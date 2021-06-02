#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 00:38:59 2021

@author: amandabreton
"""
# help from here: 
# http://myinspirationinformation.com/uncategorized/audio-signals-in-python/
#import libraries
import urllib
import scipy.io.wavfile
import pydub
import os 
import random 
import numpy as np
from numpy import fft as fft
import matplotlib.pyplot as plt

path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
files = os.listdir(path)
sound = os.path.join(path, random.choice(files))

rate,audData=scipy.io.wavfile.read(sound)
print('sampling rate = '), print(rate)
#print('audio wave data = '),print(audData)
audlength = audData.shape[0]/rate

#power - energy per unit of time
power = 1.0/(2*(audData.size)+1)*np.sum(audData.astype(float)**2)/rate

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

plt.figure(2, figsize=(8,6))
Pxx, freqs, bins, im = plt.specgram(audData, Fs=rate, NFFT=1024)
cbar=plt.colorbar(im)
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
cbar.set_label('Intensity dB')

# this doesn't work: 
#where  = np.where(freqs==2000)
#MHZ10=Pxx[where,:]
#plt.plot(bins, MHZ10, color='#ff7f00')
#plt.show()

#it's 1:09am so I'm going to stop for now and continue in the morning 
