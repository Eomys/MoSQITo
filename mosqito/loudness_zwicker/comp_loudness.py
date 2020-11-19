# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:23:56 2020

@author: martin_g for eomys
"""

# Standard import
import numpy as np

# Local imports
from mosqito.loudness_zwicker.loudness_zwicker_stationary import loudness_zwicker_stationary
from mosqito.loudness_zwicker.loudness_zwicker_time import loudness_zwicker_time      
    
def comp_loudness(is_stationary, spec_third, third_axis=[], field_type = 'free'):
    """  Acoustic loudness calculation according to Zwicker method for
    stationary and time-varying signals.
    
    Parameters
    ----------
    is_stationary: boolean
        TRUE if the signal is stationary, FALSE if it is time-varying
    spec_third: numpy.array
        third-octave spectrum
    third_axis: numpy.array
        third-octave spectum frequency axis
    field-type: string
        'free' by default or 'diffuse'
    
    Outputs
    -------
    N: float/numpy.array
        loudness value
    N_specific: numpy.array
        specific loudness values
    bark_axis: numpy.array
        frequency axis correpsondong to N_specific values in bark
    
    """

    if is_stationary == True:
        N, N_specific = loudness_zwicker_stationary(spec_third, third_axis, field_type)
    elif is_stationary == False: 
        N, N_specific = loudness_zwicker_time(spec_third, field_type)
    
    # critical band rate scale
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))  
    
    return N, N_specific, bark_axis
    