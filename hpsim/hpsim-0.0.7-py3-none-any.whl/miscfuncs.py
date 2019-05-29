#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:52:47 2019

@author: hogbobson
"""
import numpy as np

class miscfuncs:
    def __init__(self):
        pass
    
    def sym_kick(self, ensemble, dt, d, forces):#, acceleration):
        ensemble['velocity'] += d * dt * self.acceleration(ensemble, forces)
        return ensemble
    
    def sym_drift(self, ensemble, dt, c):
        ensemble['r'] += c * dt * ensemble['velocity']
        ensemble['distance'] = self.distances(ensemble['r'])
        return ensemble
    
    def acceleration(self, ensemble, forces): #save this in the class?
        acc = np.zeros_like(ensemble['r'])
        for force_func in forces:
            acc += force_func(ensemble['distance'], ensemble['mass'])
        return acc
    
    def distances(self, vec): # There must be an easier way.
        """ Converts matrix elements from origin -> object to object -> object. \
        Naturally, the dimensions in the matrix increase because of that. """
        newr = np.zeros((np.shape(vec)[0],np.shape(vec)[0],3))
        for i in range(3):  #For future: get rid of loop, if possible.
            newr[:,:,i] = vec[:,i].reshape(1,np.size(vec[:,i])) - \
            vec[:,i].reshape(np.size(vec[:,i]),1)
        return newr 