# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:17:27 2020

@author: wantysal
"""
# Standard library import
import numpy as np


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
    
    # # Amplitude modulated signal
    signal = np.power(10,dB/20)*2e-05*2**0.5*(1 + mdepth * (np.cos(2*np.pi*fmod*time))) * np.cos(2*np.pi*fc*time)    
    
    
    # signal = 0.5*(1 + mdepth * (np.sin(2*np.pi*fmod*time))) * np.sin(2*np.pi*fc*time)    
    # rms = np.sqrt(np.mean(np.power(signal,2)))
    # ampl = 2*10**(-3/20)*np.power(10,0.05*dB)/rms
    # signal = signal * ampl
    
    
    return signal
    
