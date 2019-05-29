#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:32:15 2019

@author: hogbobson
"""
import numpy as np
from numpy import linalg as LA
from astropy import constants as astcnst

def gravity(r,M):
    """ Compute gravitational acceleration at r,
    shamelessly copied from 7a in computational astrophysics. """
    rm = LA.norm(r,axis = 2)     # Find the magnitude of distances (usually SSO.d is loaded in here)
    rm[rm == 0] = np.nan    # Make 0s nan so we avoid divide by 0.
    rmcub = rm*rm*rm        # They say rm*rm*rm is faster than rm**3
    a = r/rmcub.reshape(np.append(np.shape(r[:,:,0]),1))    # This was surprisingly hard to get working
    a *= astcnst.G.value*M.reshape(1,np.size(M),1)             # So I do it one step at a time.
    a[np.isnan(a)] = 0      # Convert nans back to 0.
    acc = np.sum(a,axis=1)  # And sum all the accelerations.
    return acc

def electrostatic():
    pass

def lennard_jones():
    pass

def spring():
    pass
