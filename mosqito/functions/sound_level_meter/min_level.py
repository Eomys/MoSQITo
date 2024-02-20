# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 19:44:20 2023

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from mosqito.utils.conversion import amp2db

def min_level(signal):
    """Calculate the minimum value of the series of levels (dB) of the one signal.

    Parameters
    ----------
    signal : numpy.array
        time signal values

    Outputs
    -------
    min_level : numpy.ndarray
        return the minimum value of the signal values.
    """
    # Empty array to store the values in dB of the signal.
    dB_values = np.zeros(signal.shape[0])
    # Performs the conversion to dB with all the values of the signal.
    for i in range(signal.shape[0]):
        #If the value is negative value.
        if signal[i] <= 0:
            # we convert it to positive.
            signal[i] = np.sqrt(np.mean(signal[i] ** 2))
        # Conversion Pa to dB.
        dB = amp2db(np.array(signal[i]))
        # Save all values in dB of the third octave in another array.
        dB_values[i] = dB
    # Save the minimum level.
    min_level = np.array(min(dB_values))

    return min_level