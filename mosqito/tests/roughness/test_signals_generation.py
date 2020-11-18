# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:17:27 2020

@author: wantysal
"""
import sys
sys.path.append('../../..')
import numpy as np
from mosqito.functions.oct3filter.oct3spec import oct3spec


def test_signal(fc, fmod, mdepth, fs, d, dB):
    """ Creation of stationary amplitude modulated signals for the roughness validation procedure
        (signal created accroding to equation 1 in "Psychoacoustical roughness:
         implementation of an optimized model" by Daniel and Weber in 1997.
    
    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency
    mdepth: float
        modulation depth
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    """
    
    # time axis definition    
    time = np.linspace(0,d,int(fs * d))
    
    # modulated signal
    signal = (1 + mdepth * (np.cos(2*np.pi*fmod*time))) * np.cos(2*np.pi*fc*time)
    
    # Compute third-octave spectrum
    spec_third, spec_freq = oct3spec(signal, fs)
    
    # Compute dB level
    level_dB = 10 * np.log10(sum(np.power(10,spec_third/10)))

    # Calibration factor to set the unmodulated signal at the desired dB level
    factor = np.power(10,(dB-level_dB)/20)
    
    # Adapt the signal
    signal = signal * factor
    
    
    
    return signal
    

   