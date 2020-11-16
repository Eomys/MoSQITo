# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 10:29:02 2020

@author: wantysal
"""
# Standard library import

import numpy as np


def gzi_definition(center_freq):
    """ Weighting function for the specific roughness given by Aures
    
    Linear interpolation from the data given in E. Zwicker, H. Fastl: Psychoacoustics, 1990 """
    
    gr_x = [ 0,1,2.5,4.9,6.5,8,9,10,11,11.5,13,17.5,21,24]
        
    gr_y = [ 0,0.35,0.7,0.7,1.1,1.25,1.26,1.18,1.08,1,0.66,0.46,0.38,0.3]
                        
    gzi = np.sqrt(np.interp(center_freq, gr_x, gr_y))
             
    return gzi