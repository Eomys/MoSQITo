# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:55:30 2020

@author: wantysal
"""

# Standard libraries imports
import numpy as np
import math
from scipy.io import wavfile


# Signal generation according to the equation given in the article
def signal_generation(duration, fc, fmod, mod, p0):
    """ 
    Amplitude-modulated signal generation
    
    The amplitude-modulated signal is created according to the equation given in the
    article "Psychoacoustical roughness: implementation of an optimized model" 
    by Daniel and Weber in 1997.
    Sampling frequency is 48 kHz.
    
    Parameters:
    -----------
    duration: integer
             signal duration in seconds 
    
    mod: float
        modulation depth
        
    fc: integer
        carrier frequency
    
    fmod: integer
        modulation frequency
        
    p0: float
        sound amplitude
        
     
    
    Output:
    -------
    signal: numpy.array
            amplitude-modulated signal
    
    """

    # Sampling frequency
    fs = 48000  
    
    # Time axis definition
    time = np.linspace(0,duration,duration*fs)
    
    am_signal = np.zeros((duration*fs))
    
    for i in range(time.size):
        am_signal[i] = p0 * (1+mod*math.cos(2*np.pi*fmod*time[i])) * math.cos(2*np.pi*fc*time[i])
    
    return am_signal



