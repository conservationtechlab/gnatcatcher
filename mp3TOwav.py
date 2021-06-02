#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:21:27 2021

@author: amandabreton
"""
import os 
#from os import path
from pydub import AudioSegment

#name = name of file you want to convert 
name = 'XC564909 - Cactus Wren - Campylorhynchus brunneicapillus.mp3'
# dst = name you want for the .wav file 
dst = "cactuswren1.wav"

path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/mp3s'
src  = os.path.join(path, name)

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

# got this error: 
#FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'
# to fix: in terminal 
#/usr/bin/ruby -e "$(curl -fsSL
#https://raw.githubusercontent.com/Homebrew/install/master/install)"  
# basically needed to install homebrew: 
# brew install ffmpeg
# this looked kind of suspicious not gonna lie 
# and took like 20 minutes to install 
# didn't work 

    