#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 14:23:41 2021

@author: amandabreton

Do not use. Was originally an attempt to convert mp3 to wav.
But mp3TOwav.py works much better.
"""
import pydub 
import numpy as np
import os 
import ffprobe

# apparently ffprobe only works with python2, and I'm running python3 
def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def write(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")

path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/mp3s'
name = 'XC564909 - Cactus Wren - Campylorhynchus brunneicapillus.mp3'
songpath = os.path.join(path, name)
sr, x = read(songpath)

#FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'