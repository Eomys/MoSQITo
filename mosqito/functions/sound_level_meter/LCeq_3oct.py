# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:02:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from Leq_3oct import Leq_3oct
#DOES NOT WORK THIS LINE I DON'T KNOW WHY
from mosqito.functions.shared.C_weighting import C_weighting

#Local imports. THIS IS NOT PART OF THE PROGRAM------------------------------------------------------------------------------------
from signal_3oct import signal_3oct

def LCeq_3oct (spectrum_signal_samples,freq):
    """Calculate the LCeq of the frequency bands you choose, returns the calculated LCeq values for each band.
    Each one is calculated with the levels (dBC) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each line is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the LCeq.

    Outputs
    -------
    Leq_freq : numpy.ndarray
        a list of the Leq values (dBC) for each frequency band.
    """
    # Empty list to keep the lists. Each list is the dBC values for each frequency band in a sample.
    signal_sample_C = []
    # Take the lines of the array one by one and perform the function to transform the values in dB to dBC.
    # Save dBC lists in the list "signal_sample_C".
    for i in range(spectrum_signal_samples.shape[0]):
        signal_sample_C.append(C_weighting(spectrum_signal_samples[i],freq))
    # Create an array in which each list of "signal_sample_C" is a line of the array.
    spectrum_signal_samples_C = np.array(signal_sample_C)
    # Calculate Leq of each frequency bands with the new dBC values.
    LCeq_3oct = Leq_3oct(spectrum_signal_samples_C, freq)

# THIS IS NOT PART OF THE PROGRAM-------------------------------------------------------------------------------------------
    print(LCeq_3oct)  
    print("hola LCeq")
#-----------------------------------------------------------------------------------------------------------------------------
    return LCeq_3oct


signal = signal_3oct()
signal_db = np.array(signal['db'])
signal_freq = signal['fr']

LCeq_3oct(signal_db, signal_freq)