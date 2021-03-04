# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:14:07 2020

@author: wantysal
"""

# Standard library import
import numpy as np



def comp_level(signal, fs, nb_points=[], start=[],stop=[]):
    """Overall Sound Pressure Level calculation from the time signal
    The SPL can be computed according to a specified number of points or 
    during a given time frame

    Parameter:
    ----------
    signal : numpy.array
        time signal value
    fs: integer
        sampling frequency
        
    Output:
    -------
    level : numpy.array
        SPL in dB

    """
    # Check the inputs
    if len(nb_points)>1:
        raise ValueError(
            "ERROR : Give a single number of points"
            )
        
    if nb_points<1 or nb_points>len(signal):
        raise ValueError(
            "ERROR : Number of points should be between 1 and the length of the given signal"
            )
    
    if start<0 or stop<0 or start>len(signal)/fs or stop>len(signal)/fs:
        raise ValueError(
            "ERROR : Time frame should be between 0s and the duration of the signal"
            )
        
    
    # Initialization
    level= []
    n = len(signal)
    
    # Case of a given number of points
    if nb_points != []:
        frame_size = int(n / nb_points)
        for i in range(nb_points):
            frame = signal[i*frame_size:i*frame_size + frame_size]
            peff = np.sqrt(np.mean(frame**2))
            level.append(10 * np.log10((peff **2/(2e-05)**2)))

    # Case of a given time frame
    if start !=[] and stop !=[]:
        frame = signal[start*fs:stop*fs]
        peff = np.sqrt(np.mean(frame**2))
        level = 10 * np.log10((peff **2/(2e-05)**2))

    return level
