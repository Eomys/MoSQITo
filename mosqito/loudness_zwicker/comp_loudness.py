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
        
    
def comp_loudness(is_stationary, spec_third, third_axis, field_type = 'free'):
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
        'free' by default or 
    
    Outputs
    -------
    N: float/numpy.array
        loudness value
    N_specific: numpy.array
        specific loudness values
    
    """
    
    
    # Check the input third-octave spectrum
    spec_third_freq = np.array([
            25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
            1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500  ])  
    
    if len(spec_third) != 28:
        raise ValueError("ERROR: spectrum must contains 28 third octave bands values")       
    elif (len(third_axis) == 28 and np.all(third_axis != spec_third_freq)) or len(third_axis) < 28:
        raise ValueError("""ERROR: third_axis does not contains 1/3 oct between 25 and 
        12.5 kHz. Check the input parameters""")
        
    # Loudness calculation
    if is_stationary == True:
        N, N_specific = loudness_zwicker_stationary(spec_third, spec_third_freq, field_type)
    elif is_stationary == False: 
        N, N_specific = loudness_zwicker_time(spec_third, field_type)
        
    return N, N_specific
    