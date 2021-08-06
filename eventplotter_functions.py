#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 23:19:23 2021

@author: amandabreton
Functions used by eventchecker.py, eventplotter.py and eventplotter_all.py
"""
import os
import pandas as pd
import numpy as np


def listtxtfiles(path):
    """Create list of txt files made by BirdNET."""
    txtfiles = []
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            name = os.path.join(path, filename)
            txtfiles.append(name)
        else:
            continue
    return txtfiles


def df_details(txtfiles, threshold):
    """Create dataframe of BirdNET species, confidences and audio sources."""
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
    return knbirds, confidences, source


def speciesplotlist(knbirds, source):
    """Create dataframe of BirdNET species, to be plotted."""
    df1 = pd.DataFrame(list(zip(knbirds, source)),
                       columns=['Species', 'Audio Source'])
    df1 = df1.groupby(df1.columns.tolist()).size().to_frame('Count').reset_index()

    specieslist = []
    [specieslist.append(x) for x in knbirds if x not in specieslist]
    speciesnum = np.arange(0, len(specieslist))
    df2 = pd.DataFrame(list(zip(specieslist, speciesnum)),
                       columns=['Species List', 'Index'])
    return specieslist, df1, df2
