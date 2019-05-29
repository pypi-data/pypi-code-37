#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:34:21 2019

@author: hogbobson
"""
import numpy as np
from numpy import random as rng, linalg as LA
from astropy import constants as astcnst
from scipy import constants as phycnst
from math import radians as rad
from hpsim.miscfuncs import distances
    
class StarSystemGenerator:
    def __init__(self):
        self.sma      = []
        self.r        = np.empty((0,3), float)
        self.rm       = []
        self.r_legacy = np.empty((0,3,0), float)
        self.v        = []
        self.vm       = []
        self.d        = []
        self.e        = []
        self.i        = []
        self.m        = []
        self.n        = 0
        self.ref      = np.empty(0,int)
        self.label    = []
        
    
    def get_ensemble(self):
        others   = {'semi major axis': self.sma,
                    'eccentricity': self.e,
                    'inclination': self.i,
                    'reference body': self.ref
                }
        
        ensemble = {'r': self.r,
                    'r magnitude': self.rm,
                    'r data': self.r_legacy,
                    'distance': self.d,
                    'velocity': self.v,
                    'velocity magnitude': self.vm,
                    'mass': self.m,
                    'number of objects': self.n,
                    'label': self.label,
                    'rem': others
                }
        return ensemble
    
    
    def set_ensemble(self, ensemble):
        self.sma      = ensemble['rem']['semi major axis']
        self.r        = ensemble['r']
        self.rm       = ensemble['r magnitude']
        self.r_legacy = ensemble['r data']
        self.v        = ensemble['velocity']
        self.vm       = ensemble['velocity magnitude']
        self.d        = ensemble['distance']
        self.e        = ensemble['rem']['eccentricity']    
        self.i        = ensemble['rem']['inclination']
        self.m        = ensemble['mass']
        self.n        = ensemble['number of objects']
        self.ref      = ensemble['rem']['reference body']
        self.label    = ensemble['label']
        
        
        
    def central_star(self, mass = astcnst.M_sun.value):
        self.r          = np.append(self.r, \
                                [[0., 0., 0.]], axis = 0)
        self.m       = np.append(self.m, mass)
        self.label.append('Sun')
        self.sma = np.append(self.sma, 0)
        self.e   = np.append(self.e, 0)
        self.i   = np.append(self.i, 0)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
    
    ##### KNOWN PLANETS #####
    def mercury(self):
        semi_major_axis = 57.91e9
        aphelion        = 69.82e9
        eccentricity    = 0.2056
        inclination     = rad(7.0)
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                                astcnst.M_earth.value*0.0553)
        self.label.append('Mercury')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
    
    def venus(self):
        semi_major_axis = 108.21e9   # Venus Semi-major axis, [m].
        aphelion        = 108.94e9   # Venus _aphelion, [m].
        eccentricity    = 0.0067     # Venus _eccentricity
        inclination     = rad(3.39)  # Venus _inclination
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                            astcnst.M_earth.value*0.815)
        self.label.append('Venus')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
        

    def earth(self):
        semi_major_axis = 149.60e9    # Earth Semi-major axis, [m].
        aphelion        = 152.1e9     # Earth _aphelion, [m].
        eccentricity    = 0.0167      # Earth _eccentricity.
        inclination     = rad(0.00005)# Earth _inclination.
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                                astcnst.M_earth.value)
        self.label.append('Earth')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
        
    
    def mars(self):
        semi_major_axis = 227.92e9    # Mars Semi-major axis, [m].
        aphelion        = 249.23e9     # Mars _aphelion, [m].
        eccentricity    = 0.0935      # Mars _eccentricity.
        inclination     = rad(1.85)# Mars _inclination.
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                                astcnst.M_earth.value * 0.107)
        self.label.append('Mars')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
        
    
    def jupiter(self):
        semi_major_axis = 778.57e9
        aphelion      = 816.62e9
        eccentricity  = 0.0489
        inclination   = rad(1.304)
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                                astcnst.M_jup.value)
        self.label.append('Jupiter')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
        
    
    def saturn(self):
        semi_major_axis = 1433.53e9
        aphelion        = 1514.50e9
        eccentricity    = 0.0565
        inclination     = rad(2.485)
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                                astcnst.M_earth.value * 95.16)
        self.label.append('Saturn')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
        
    
    def uranus(self):
        semi_major_axis = 2872.46e9
        aphelion        = 3003.62e9
        eccentricity    = 0.0457
        inclination     = rad(0.772)
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                                astcnst.M_earth.value * 14.54)
        self.label.append('Uranus')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
        
    
    def neptune(self):
        semi_major_axis = 4495.06e9
        aphelion        = 4545.67e9
        eccentricity    = 0.0113
        inclination     = rad(1.769)
        self.r          = np.append(self.r, \
                            [[aphelion, 0., 0.]], axis = 0)
        self.m       = np.append(self.m, \
                                astcnst.M_earth.value * 17.15)
        self.label.append('Neptune')
        self.sma = np.append(self.sma, \
                                semi_major_axis)
        self.e   = np.append(self.e, \
                                eccentricity)
        self.i   = np.append(self.i, \
                                inclination)
        self.ref = np.append(self.ref, 0)
        self.n  += 1
    ##### END KNOWN PLANETS #####
    
    def all_known_planets(self):
        self.mercury()
        self.venus()
        self.earth()
        self.mars()
        self.jupiter()
        self.saturn()
        self.uranus()
        self.neptune()
        
    def random_planets(self, num_ran_planets):
        def log_uniform(low = 1, high = 2, size = 1, base = 10):
            return np.power(base, rng.uniform(low, high, size))
        
        for i in range(num_ran_planets):
            x = log_uniform(9, 11)
            y = log_uniform(9, 11)
            z = log_uniform(0, 7)
            r = np.reshape(np.array([x, y, z]), (1,3))
            m = np.maximum(rng.randn()+3, 1e-5)*astcnst.M_earth.value*1e-3
            rmax = LA.norm(np.array([x, y, z]), axis = 0)
            e = np.minimum(np.abs(rng.randn()*0.1), 0.95)
            sma = rmax / (1 + e)
            i = np.arccos(z/rmax)
            self.r = np.append(self.r, r, axis = 0)
            self.m = np.append(self.m, m)
            self.label.append('random planet #' + str(i))
            self.sma = np.append(self.sma, sma)
            self.e = np.append(self.e, e)
            self.i = np.append(self.i, i)
            self.ref = np.append(self.ref, 0)
            self.n += 1
                    
    
    def velocities_with_central_star(self):
        """ Makes the rm vector and sets the velocities, 
        as per parametres. """
        n = self.n
        self.d  = distances(self.r)
        #dm             = LA.norm(self.d, axis = 2)
        self.rm = LA.norm(self.r, axis = 1)
        theta_v = np.zeros(n)
        theta_v[1:n] = np.pi/2 - \
                np.arctan(np.abs(self.r[1:n, 1]/self.r[1:n, 0]))
        self.vm = np.zeros_like(self.m)
        self.vm[1:n] = np.sqrt(astcnst.G.value * \
                        self.m[0] * (2/self.rm[1:n] - \
                        1/self.sma[1:n]))
        alpha = np.reshape(np.sqrt(1. - self.e**2), (n, 1))
        self.v  = np.zeros_like(self.r)
        self.v[:n,0] = -1 * np.sign(self.r[:n,1]) * \
                        np.cos(theta_v[:n]) * self.vm[:n]
        self.v[:n,1] = np.sign(self.r[:n,0]) * \
                        np.cos(theta_v[:n]) * self.vm[:n]
        self.v[:n,:] = self.v[:n,:] * alpha[:n]
        self.v[:n,2] = self.vm - LA.norm(self.v[:n,:], axis = 1)
        self.vm = LA.norm(self.v, axis = 1)
        self.r_legacy = np.reshape(self.r, (n, 3, 1))
    
    
    
    #for ith_dict in generator_list:
    #    ensemble = ith_dict['function name(ensemble, ith_dict['arg)
        
    #return ensemble

def solar_system():
    SSG = StarSystemGenerator()
    SSG.central_star()
    SSG.all_known_planets()
    SSG.velocities_with_central_star()
    
    ensemble = SSG.get_ensemble()
    return ensemble
    
def random_solar_system():
    SSG = StarSystemGenerator()
    SSG.central_star()
    SSG.random_planets(10)
    SSG.velocities_with_central_star()
    
    ensemble = SSG.get_ensemble()
    return ensemble
