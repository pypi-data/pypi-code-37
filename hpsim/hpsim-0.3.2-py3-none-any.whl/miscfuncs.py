#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:52:47 2019

@author: hogbobson
"""
import numpy as np

def sym_kick(ensemble, dt, d, forces):#, acceleration):
    ensemble['velocity'] += d * dt * acceleration(ensemble, forces)
    return ensemble

def sym_drift(ensemble, dt, c):
    ensemble['r'] += c * dt * ensemble['velocity']
    ensemble['distance'] = distances(ensemble['r'])
    return ensemble

def acceleration(ensemble, forces): #save this in the class?
    acc = np.zeros_like(ensemble['r'])
    for force_func in forces:
        acc += force_func(ensemble['distance'], ensemble['mass'])
    return acc

def distances(vec): # There must be an easier way.
    """ Converts matrix elements from origin -> object to object -> object. \
    Naturally, the dimensions in the matrix increase because of that. """
    newr = np.zeros((np.shape(vec)[0],np.shape(vec)[0],3))
    for i in range(3):  #For future: get rid of loop, if possible.
        newr[:,:,i] = vec[:,i].reshape(1,np.size(vec[:,i])) - \
        vec[:,i].reshape(np.size(vec[:,i]),1)
    return newr 