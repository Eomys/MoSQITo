# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 09:04:04 2020

@author: pc
"""
import numpy as np

def critical_band(f0):
    """ Analytical definition of the critical band centered on f0
    according to ECMA-74 annex D.8"""
    
    delta_fc = 25 + 75 * np.power(1 + 1.4 * np.power(f0 / 1000, 2), 0.69)
    
    if f0 >= 89.1 and f0 < 500:
        f1 = f0 - delta_fc / 2
        f2 = f0 + delta_fc / 2
        
    elif f0 >= 500 and f0 <= 11200:
        f1 = -1 * delta_fc / 2 + np.sqrt(delta_fc ** 2 + 4 * f0 ** 2) / 2
        f2 = f1 + delta_fc
    else:
        f1 = None
        f2 = None
        
    return f1, f2
    
    
    