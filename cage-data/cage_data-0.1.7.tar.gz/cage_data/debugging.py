# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 10:15:17 2019

@author: xuan
"""
from brpylib import NevFile 
import numpy as np
filename = 'D:/cage_data/20190123_Greyson_Cage_003.nev'
nev_file = NevFile(filename)
chans = list(np.arange(1, 10, 1))
nev_data = nev_file.getdata(chans)
spike_events = nev_data['spike_events']
nev_file.close()