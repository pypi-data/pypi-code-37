#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:32:53 2019

@author: hogbobson
"""
import numpy as np
    
def time_seconds(seconds):
    return seconds

def time_minutes(minutes):
    return self.time_seconds(60*minutes)

def time_hours(hours):
    return self.time_minutes(60*hours)

def time_days(days):
    return self.time_hours(24*days)

def time_months(months):
    return self.time_days(30*months)

def time_years(years): #You cant top the elegance of pi*1e7!
    return np.pi * 1e7 * years

def time_years_precise(years):
    return self.time_days(365.256363004*years)

def time_Myr(mega_years):
    return self.time_years(1e6*mega_years)
