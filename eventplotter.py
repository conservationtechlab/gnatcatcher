#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 20:01:53 2021

@author: amandabreton
"""
# set up modules and paths
import pandas as pd
import os
import numpy as np
import exiftool
import matplotlib.pyplot as plt
import argparse
import yaml

# %% setup your paths
parser = argparse.ArgumentParser()
parser.add_argument('config_filename')
args = parser.parse_args()
CONFIG_FILE = args.config_filename
with open(CONFIG_FILE) as f:
    configs = yaml.load(f, Loader=yaml.SafeLoader)
path = configs['path']
threshold = configs['threshold']
# %%
# path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/sounds/'
# threshold = 0.8
# %%
files = os.listdir(path)  # Get all the files in that directory
txtfiles = []
for filename in os.listdir(path):
    if filename.endswith(".txt"):
        name = os.path.join(path, filename)
        txtfiles.append(name)
    else:
        nonimagecount = +1
        continue
# %%

knbirds = []
source = []
confidences = []
for k in range(len(txtfiles)):
    birdtxt = txtfiles[k]
    df = pd.read_csv(birdtxt, sep='\t')
    for i in range(1, len(df)):
        confid = df['Confidence'][i]
        confid = float(confid)
        if confid > threshold:
            # knbirds.append(confid)
            bird = df['Common Name'][i]
            knbirds.append(bird)
            audio = df['Begin File'][i]
            source.append(audio)
            confidences.append(confid)
        else:
            pass

df = pd.DataFrame(list(zip(knbirds, confidences, source)),
                  columns=['Species', 'Confidence', 'Audio Source'])

# %% setting up stuff to graph
df1 = pd.DataFrame(list(zip(knbirds, source)),
                   columns=['Species', 'Audio Source'])
df1 = df1.groupby(df1.columns.tolist()).size().to_frame('Count').reset_index()

specieslist = []
[specieslist.append(x) for x in knbirds if x not in specieslist]

# %%
print('Here are the species you can plot:')
print(specieslist)
print('Which species would you like to investigate further?')
bird = input()
# %%
sources = []
count = []
times = []
comments = []

for i in range(len(df1['Audio Source'])):
    if bird == str(df1['Species'][i]):
        audsource = (df1['Audio Source'][i])
        sources.append(audsource)
        freq = (df1['Count'][i])
        count.append(freq)
        exifpath = str(path) + str(df1['Audio Source'][i])
        with exiftool.ExifTool() as et:
            audComment = et.get_tag("Comment", exifpath)
        time = audComment[13:20]
        comments.append(audComment)
        times.append(time)
    else:
        pass

df2 = pd.DataFrame(list(zip(times, sources, count)),
                   columns=['Time', 'Audio Source', 'Count'])
# %%
df2.plot.bar(x='Time', y='Count', rot=0)
plt.xlabel("Time")
plt.ylabel("Count")
plt.title(bird)
plt.show()
