import numpy as np 
import statsmodels as sm 
import math
import matplotlib.pyplot as plt 
from scipy.integrate import quad
import sys
import os
import logging
from brd_mod.brdstats import *
from brd_mod.brdecon import *


def meter_to_mi(x):
	'''
	Converts a parameter in metres to miles
	using a standard conversion factor.
	'''
	return 0.000621371*x

def deg_to_rad(x):
	'''
	Converts a parameter in degrees to radians
	'''
	return (math.pi*x)/180

def haversine_distance(t_a, n_a, t_b, n_b):
	'''
	Returns distance between two coordinates using
	the Haversine formula
	'''
	lat_a= deg_to_rad(t_a)
	lon_a= deg_to_rad(n_a)
	lat_b= deg_to_rad(t_b)
	lon_b= deg_to_rad(n_b)

	R= 6373000
	delta_lat= lat_b - lat_a
	delta_lon= lon_b - lon_a
	a_var= np.sin(delta_lat/2)**2 + np.cos(lat_a)  \
		* np.cos(lat_b) * np.sin(delta_lon/2)**2
	c_var= 2*(np.arctan2(math.sqrt(a_var), math.sqrt(1-a_var)))
	return meter_to_mi(R*c_var)