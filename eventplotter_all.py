#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 23:18:49 2021

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
import eventplotter_functions as epf
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

# %% use epf.listtxtfiles to create list of txt files made by BirdNET.
txtfiles = epf.listtxtfiles(path)

# %% Create dataframe of BirdNET species, confidences and audio sources
knbirds, confidences, source = epf.df_details(txtfiles, threshold)

# %% setting up stuff to graph
specieslist, df1, df2 = epf.speciesplotlist(knbirds, source)

# %%  plotting all the spceise
print('Here are the species being plotted:')
print(specieslist)

for k in range(len(specieslist)):
    bird = specieslist[k]
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
    df2.plot.bar(x='Time', y='Count', rot=0)
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.title(bird)
plt.show()
