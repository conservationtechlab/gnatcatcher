#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 23:41:32 2021

@author: amandabreton

Creates a csv file for the ground truth data used to test micorfaune.

"""
# %% import utilities and paths
import os
from os import walk
import pandas as pd
import argparse
import yaml
# %% parse in paths
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
otherpath = configs['otherpath']
anipath = configs['anipath']

# %%
other = next(walk(otherpath), (None, None, []))[2]  # [] if no file
animals = next(walk(anipath), (None, None, []))[2]

othermarker = []
for i in range(len(animals)):
    i = 0
    othermarker.append(i)

animarker = []
for i in range(len(animals)):
    i = 1
    animarker.append(i)

# %%
allaudio = other + animals
allmarkers = othermarker + animarker

# %% create dataframe
df = pd.DataFrame(list(zip(allaudio, allmarkers)),
                  columns=['Audio', 'Marker'])
df.to_csv()
