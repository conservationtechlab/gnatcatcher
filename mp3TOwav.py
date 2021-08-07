#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:21:27 2021

@author: amandabreton
"""
# import required modules
import subprocess
from os import walk
from glob import glob
import os
import argparse
import yaml
# %% parse in paths
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
mp3path = configs['mp3path']
wavpath = configs['wavpath']

# %% remove DS store file (mac issue)
if os.path.exists(os.path.join(mp3path, ".DS_Store")):
    os.remove(os.path.join(mp3path, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

# %% get file lists

file_list = glob('/Users/amandabreton/Documents/GitHub/gnatcatcher/mp3s/*.mp3')
mp3files = next(walk(mp3path), (None, None, []))[2]  # [] if no file

# %%
os.chdir(wavpath)
for i in range(len(mp3files)):
    soundname = mp3files[i][:-4]
    mp3 = file_list[i]
    subprocess.call(['ffmpeg', '-i', mp3,
                     str(soundname) + '.wav'])
