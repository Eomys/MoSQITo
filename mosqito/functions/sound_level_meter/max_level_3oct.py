# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 15:10:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

#Local imports. THIS IS NOT PART OF THE PROGRAM------------------------------------------------------------------------------------
from signal_3oct import signal_3oct

def max_level_3oct(spectrum_signal_samples, freq):
    """Return the maximum value of the frequency bands you choose. Each one is calculated with the levels (dB)
    of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each line is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the Leq.

    Outputs
    -------
    max_level_3oct : numpy.ndarray
        the maximum values of each frequency band.
    """
    # Empty array to keep the levels (dB) of each one of the samples of a specific frequency band.
    main_freq = np.zeros(spectrum_signal_samples.shape[0])
    # Empty array to store the maximum values of each frequency band.
    max_level_3oct = np.zeros(freq.shape[0])
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]):
        # Save the values of a frequency band.
        for j in range(spectrum_signal_samples.shape[0]):
            main_freq[j] = spectrum_signal_samples[j,i]
        # Calculate the maximum with the values.
        max_level_3oct[i] = max(main_freq) 

#this is not part of the program-----------------------------------------------------------------------------------------
        #print(freq[i])
    print(max_level_3oct)
#-------------------------------------------------------------------------------------------------------------------------
    
    return max_level_3oct


signal = signal_3oct()
signal_db = np.array(signal['db'])
signal_freq = signal['fr']

max_level_3oct(signal_db, signal_freq)