#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 10:16:27 2021

@author: amandabreton

Used to see if stereo audio files can be changed to mono so
that microfaune can analyze them. Once you run this you should
be able to run microfaune on the folder of mono audio files
Note: this saves whole new audio files because of how microfaune works
"""
# import utilities
import os
from os import walk
from pydub import AudioSegment
from glob import glob
import argparse
import yaml
# %%  yaml file example:
# stereopath is path to audio with stereo channels
# stereopath = '/Users/amandabreton/Documents/GitHub/gnatcatcher/Ground Truth Sounds/animals_stereo'
# monopath is path to where you want the new mono files saved
# monopath = '/Users/amandabreton/Documents/GitHub/gnatcatcher/Ground Truth Sounds/new_mono/'

# %% setup your files
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
stereopath = configs['stereopath']
monopath = configs['monopath']

# %% remove DS store file (mac issue)
if os.path.exists(os.path.join(stereopath, ".DS_Store")):
    os.remove(os.path.join(stereopath, ".DS_Store"))
else:
    # print("no .DS_Store files")
    pass

# %% set up the stereo files
file_list = glob(str(stereopath)+'/*.wav')
stereofiles = next(walk(stereopath), (None, None, []))[2]  # [] if no file


# %%
os.chdir(monopath)
for i in range(len(stereofiles)):
    soundname = stereofiles[i][:-4]
    stereo = file_list[i]
    sound = AudioSegment.from_wav(file_list[i])
    sound = sound.set_channels(1)
    sound.export(str(monopath) + soundname, format="wav")
