#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:21:27 2021

@author: amandabreton
"""
#import utilities
import os 
#from os import path
from pydub import AudioSegment
from glob import glob

# set up paths
file_list = glob('/Users/amandabreton/Documents/GitHub/gnatcatcher/mp3s/*.mp3')
path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/mp3s'

for i in range(len(file_list)):
    name = file_list[i]
    sound = AudioSegment.from_mp3(name)
    sound.export(name, format= "wav")


# %%
#name = name of file you want to convert
name = 'XC564909 - Cactus Wren - Campylorhynchus brunneicapillus.mp3'
# dst = name you want for the .wav file 
dst = "cactuswren1.wav"


src  = os.path.join(path, name)

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")
