#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:21:18 2021

@author: amandabreton
"""

from opensoundscape.preprocess.preprocessors import AudioToSpectrogramPreprocessor
# The cnn module provides classes for training/predicting with various types of CNNs
from opensoundscape.torch.models.cnn import Resnet18Binary
from opensoundscape.helpers import run_command
# Other utilities and packages
import torch
from pathlib import Path
import numpy as np
import pandas as pd
from glob import glob
#set up plotting
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize']=[15,5] #for large visuals
# %config InlineBackend.figure_format = 'retina'

# collect a list of audio files
# this is the path to the audio you want to analyze
# file_list = glob('./woodcock_labeled_data/*.wav')
file_list = glob('./sounds/*.WAV')
# create a DataFrame with the audio files as the index
audio_file_df = pd.DataFrame(index=file_list)

# create a Preprocessor object
# we use the option "return_labels=False" because our audio to predict on does not have labels
from opensoundscape.preprocess.preprocessors import AudioToSpectrogramPreprocessor
prediction_dataset = AudioToSpectrogramPreprocessor(audio_file_df, return_labels=False)

from opensoundscape.torch.models.cnn import PytorchModel
from opensoundscape.torch.architectures.cnn_architectures import resnet18
import torch

# load the tar file into a dictionary
# (you could change this to the location of any .tar file on your computer)
opso_04_model_tar_path = "./opso_04_model_acanthis-flammea.tar"
opso_04_model_dict = torch.load(opso_04_model_tar_path)

# create a resnet18 binary model
# (all models created with Opensoundscape 0.4.x are 2-class resnet18 architectures)
architecture = resnet18(num_classes=2,use_pretrained=False)
model = PytorchModel(classes=['negative','positive'],architecture=architecture)

# load the model weights into our model object
# now, our model is equivalent to the trained model we downloaded
model.network.load_state_dict(opso_04_model_dict['model_state_dict'])

# generate predictions on our dataset
predition_scores_df,_,_ = model.predict(prediction_dataset, activation_layer='softmax_and_logit')

predition_scores_df.head(3)
print(predition_scores_df)
