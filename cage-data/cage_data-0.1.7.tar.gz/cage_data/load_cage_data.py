# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 20:31:04 2019

@author: xuan
"""

#%%
from cage_data import cage_data
path = 'D:/cage_data'
nev_file = '20190123_Greyson_Cage_003.nev'
rhd_file = '20190123_Greyson_Cage__190123_104515.rhd'
cage_20190123_003 = cage_data()
cage_20190123_003.create(path, nev_file, rhd_file, [7, 79])
cage_20190123_003.clean_cortical_data()
cage_20190123_003.bin_spikes(0.05)
cage_20190123_003.smooth_binned_spikes('gaussian', 0.05, sqrt = 1)
cage_20190123_003.EMG_filtering(10)
cage_20190123_003.EMG_downsample(1/0.05)
filtered_EMG = cage_20190123_003.filtered_EMG
binned_spike = cage_20190123_003.binned_spikes
timeframe = cage_20190123_003.nev_timeframe
#%%
cage_20190123_003.pre_processing_summary()
cage_20190123_003.save_to_pickle('D:/cage_data/20190123_Greyson_Cage_003.pkl')
#%%
import _pickle as pickle
with open ('D:/cage_data/sorted/20181221_Greyson_Cage_003-01.pkl', 'rb') as fp:
    my_cage_data = pickle.load(fp)
waveforms = my_cage_data.waveforms
#import matplotlib.pyplot as plt
#plt.plot(waveforms[40].T)
#    
#%%
import numpy as np
binned_spike = np.asarray(binned_spike)
filtered_EMG = np.asarray(filtered_EMG)

#%%
from cage_data import cage_data
path = 'D:/cage_data'
nev_file = '20181221_Greyson_Cage_003-01.nev'
rhd_file = '20181221_Greyson_Cage__181221_101423.rhd'
cage_20181221_002 = cage_data()
cage_20181221_002.create(path, nev_file, rhd_file, [7, 79])
#cage_20181221_002.clean_cortical_data()
cage_20181221_002.bin_spikes(0.05)
cage_20181221_002.smooth_binned_spikes('gaussian', 0.05, sqrt = 1)
cage_20181221_002.EMG_filtering(10)
cage_20181221_002.EMG_downsample(1/0.05)
filtered_EMG = cage_20181221_002.filtered_EMG
binned_spike = cage_20181221_002.binned_spikes
timeframe = cage_20181221_002.nev_timeframe
#%%
cage_20181221_002.pre_processing_summary()
cage_20181221_002.save_to_pickle('D:/cage_data/20181221_Greyson_Cage_003.pkl')


