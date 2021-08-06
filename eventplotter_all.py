#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 23:18:49 2021

@author: amandabreton
Plots and saves the bird vocalizations found by eventplotter.
Outputs a graph for every single probable species above
the given threshold and found inside the San Diego Zoo
BioDiversity Reserve. The user does not need to tell the script
which species they would like to investigate further.
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
biodiversity_reserve_bird_list = configs['biodiversity_reserve_bird_list']
# %% yaml file example 
# path = '/Users/amandabreton/Documents/GitHub/gnatcatcher/audiomoth_data/reserve/yucca/'
# threshold = 0.8
# biodiversity_reserve_bird_list = '/Users/amandabreton/Documents/GitHub/gnatcatcher/reservebirds.csv'
# %% use epf.listtxtfiles to create list of txt files made by BirdNET.
txtfiles = epf.listtxtfiles(path)
graphfolder = 'Reserve_Graphs/'
graphpath = os.path.join(path, graphfolder)
# os.mkdir(graphpath)
if not os.path.exists(graphpath):
    os.makedirs(graphpath)
# %% Create dataframe of BirdNET species, confidences and audio sources
knbirds, confidences, source = epf.df_details(txtfiles, threshold)

# %% setting up stuff to graph
specieslist, df1, df2 = epf.speciesplotlist(knbirds, source)

# %% getting the list of birds actually in the reserve
BRBLdf = pd.read_csv(biodiversity_reserve_bird_list, header=0)
reservebirds = BRBLdf['COMMON']

foundinreserve = []
for i in range(len(specieslist)):
    bird = specieslist[i]
    if reservebirds.str.contains(bird).any():
        foundinreserve.append(bird)
# %%  plotting all the spceise
print('Here are all the species above the threshold')
print(specieslist)

print('These are the most probable species based on location:')
print(foundinreserve)
print('They will be plotted now.')
print('If you want to plot the other birds, please use eventplotter.py')
# %%
for k in range(len(foundinreserve)):
    bird = foundinreserve[k]
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
            time = audComment[12:17]
            date = audComment[20:31]
            comments.append(audComment)
            times.append(time + date)
        else:
            pass
    df2 = pd.DataFrame(list(zip(times, sources, count)),
                       columns=['Time', 'Audio Source', 'Count'])
    df2.plot.bar(x='Time', y='Count', rot=0)
    plt.xlabel("Time and Date")
    plt.ylabel("Number of Vocalizations")
    plt.title(bird)
    plt.gca().set_yticks(df2["Count"].unique())
    plt.savefig(graphpath + bird)
plt.show()
