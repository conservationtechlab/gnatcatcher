#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:45:09 2021

@author: amandabreton
"""
# 
#import the pyplot and wavfile modules 
import matplotlib.pyplot as plot
from scipy.io import wavfile
from playsound import playsound
import argparse 
import yaml 
import os 
import random
import wave
import contextlib
from scipy.fft import fft, ifft, fftfreq
# learning stuff from here: 
# https://makersportal.com/blog/2018/9/13/audio-processing-in-python-part-i-sampling-and-the-fast-fourier-transform

parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename

with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
    
path = configs['path']
#path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds'
files = os.listdir(path)
sound = os.path.join(path, random.choice(files))

# Read the wav file (mono)
samplingFrequency, signalData = wavfile.read(sound)
wavdata = wave.open(sound, 'r')
print ( "parameters:",wavdata.getparams())

# Plot the signal read from wav file
plot.subplot(211)
plot.title('Recorded Sound')
plot.plot(signalData)
plot.xlabel('Sample')
plot.ylabel('Amplitude')

plot.subplot(212)
plot.title('Spectrogram')
plot.specgram(signalData,Fs=samplingFrequency)
plot.xlabel('Time (sec)')
plot.ylabel('Frequency (Hz)')
plot.show()

#playsound(sound)

with contextlib.closing(wave.open(sound,'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print('Duration of sound:')
    print(duration)

#yf = fft(signalData)
