#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 19:46:43 2019

@author: hogbobson
"""

import numpy as np
from matplotlib import pyplot as plt


class visual:
    def __init__(self):
        pass
    
    def no_plot(self, ensemble):
        pass
    
    def standard_plot(self, ensemble):
        n = ensemble['number of objects']
        plt.figure(num = 0, figsize = (8,8))
        for i in range(n):
            plt.plot(ensemble['r data'][i,0,:], ensemble['r data'][i,1,:], '-', \
                     label = ensemble['label'][i], \
                     color = (abs(np.sin(i)), 0 + i/n, 1-i/n))
        plt.xlabel('x')
        plt.ylabel('y')
        xlim = np.max(ensemble['r data'])*1.1
        xlim = 5*1e11
        plt.axis((-xlim, xlim, -xlim, xlim))
        plt.legend()
        plt.show()
