# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 19:45:20 2023

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from mosqito.utils.conversion import amp2db

def LN(signal):
    """Calculate the percentile value of the series of levels (dB) of the one signal.  

    Parameters
    ----------
    signal : numpy.array
        time signal values [Pa]

    Outputs
    -------
    percentiles : numpy.ndarray
        The values in dB of L90, L50 and L25 of the signal.
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
    # Calculate the percentiles with the values. "q" of np.percentile = 100 - N (N of LN).
    L90 = np.percentile(dB_values, 10,interpolation='linear') 
    L50 = np.percentile(dB_values, 50,interpolation='linear') 
    L25 = np.percentile(dB_values, 75,interpolation='linear')
    # Save the calculated percentile values.
    percentiles = np.array([L90,L50,L25])

    return percentiles