#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:32:53 2019

@author: hogbobson
"""
import numpy as np

class timegen:
    def __init__(self):
        pass
    
    def time_seconds(self, seconds):
        return seconds

    def time_minutes(self, minutes):
        return self.time_seconds(60*minutes)
    
    def time_hours(self, hours):
        return self.time_minutes(60*hours)
    
    def time_days(self, days):
        return self.time_hours(24*days)
    
    def time_months(self, months):
        return self.time_days(30*months)
    
    def time_years(self, years): #You cant top the elegance of pi*1e7!
        return np.pi * 1e7 * years
    
    def time_years_precise(self, years):
        return self.time_days(365.256363004*years)
    
    def time_Myr(self, mega_years):
        return self.time_years(1e6*mega_years)
