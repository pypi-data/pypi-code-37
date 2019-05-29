#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:39:28 2019

@author: hogbobson
"""

import numpy as np
import force
import solver
import ntgrtr
import ensgen
import timestep
import timegen
import visual

class sonic:
    def __init__(self, ensemble_generator = ensgen.solar_system, \
                       integration_func = ntgrtr.n_squared, \
                       solver_func = solver.sym2, \
                       wanted_forces = [force.gravity], \
                       plot_func = visual.standard_plot, \
                       time_start = 0, \
                       time_step = timestep.constant_dt(100000), \
                       time_end = timegen.time_years(1)):
    
        everything = {
                'ensemble': ensemble_generator(),
                'integrator': integration_func,
                'solver': solver_func,
                'forces': wanted_forces,
                'plotter': plot_func,
                'time start': time_start,
                'current time': time_start,
                'dt': time_step,
                'time end': time_end
                }
        
        #I put everything here that isn't changed for readability.
        integrator = everything['integrator']
        solver     = everything['solver']
        forces     = everything['forces']
        
        while everything['current time'] < everything['time end']:
            integrator(everything['ensemble'])
            solver(everything['ensemble'], everything['dt'], forces)
            everything['current time'] += everything['dt']
            everything['ensemble']['r data'] = np.append( \
                      everything['ensemble']['r data'], 
                      np.reshape(everything['ensemble']['r'], \
                            (everything['ensemble']['number of objects'], \
                             3,1)), axis = 2)
        
        plot_func(everything['ensemble'])
    
        self.everything = everything
