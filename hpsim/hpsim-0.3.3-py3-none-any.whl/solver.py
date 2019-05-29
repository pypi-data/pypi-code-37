#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:29:19 2019

@author: hogbobson
"""
from hpsim.miscfuncs import sym_kick, sym_drift

def sym1(ensemble, dt, forces):
    ensemble = sym_kick(ensemble, dt, 1, forces)
    ensemble = sym_drift(ensemble, dt, 1)
    return ensemble
    
def sym2(ensemble, dt, forces):
    ensemble = sym_kick(ensemble, dt, 0.5, forces)
    ensemble = sym_drift(ensemble, dt, 1)
    ensemble = sym_kick(ensemble, dt, 0.5, forces)
    return ensemble

def sym3(ensemble, dt, forces):
    pass

#Figure out how to make these two v^ not awful.

def sym4(ensemble, dt, forces):
    pass
