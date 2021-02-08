# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:14:07 2020

@author: wantysal
"""

# Standard library import
import numpy as np

# Local import
from mosqito.functions.shared.conversion import spectrum2dBA


def comp_level(is_stationary, spec_third, fs, unit):
    """ Overall Sound Pressure Level calculation in the chosen unit 
    from the signal's third-octave spectrum
        
    Parameter:
    ----------
    spec_third_dB: numpy.array
        third octave spectrum of the signal 
    fs: integer
        sampling frequency
    unit : string
        'dB' or 'dBA'
            
    """        

    if unit =='dB':
        level = 10 * np.log10(sum(np.power(10,spec_third['values']/10)))       
        
    elif unit =='dBA':
        # spectrum A-weighting
        spec_third_dBA = spectrum2dBA(spec_third['values'],fs)
        level = 10 * np.log10(sum(np.power(10,spec_third_dBA/10)))

    return level