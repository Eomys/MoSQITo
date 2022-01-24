# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:02:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from Leq_3oct import Leq_3oct
from mosqito.functions.shared.A_weighting import A_weighting

#Local imports. THIS IS NOT PART OF THE PROGRAM------------------------------------------------------------------------------------
from signal_3oct import signal_3oct

def LAeq_3oct (spectrum_signal_samples,freq):
    """Calculate the LAeq of the frequency bands you choose, returns the calculated LAeq values for each band.
    Each one is calculated with the levels (dBA) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each line is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the LAeq.

    Outputs
    -------
    Leq_freq : numpy.ndarray
        a list of the Leq values (dBA) for each frequency band.
    """
    # Empty list to keep the lists. Each list is the dBA values for each frequency band in a sample. 
    signal_sample_A = []
    # Take the lines of the array one by one and perform the function to transform the values in dB to dBA.
    # Save dBA lists in the list "signal_sample_A". 
    for i in range(spectrum_signal_samples.shape[0]):
        signal_sample_A.append(A_weighting(spectrum_signal_samples[i],freq))
    # Create an array in which each list of "signal_sample_A" is a line of the array. 
    spectrum_signal_samples_A = np.array(signal_sample_A)
    # Calculate Leq of each frequency bands with the new dBA values. 
    LAeq_3oct = Leq_3oct(spectrum_signal_samples_A, freq)
    
    # THIS IS NOT PART OF THE PROGRAM-----------------------------------------------------------------------------------------
    #print(spectrum_signal_samples_A)
    print(LAeq_3oct)  
    print("hola LAeq")
    #-------------------------------------------------------------------------------------------------------------------------
    
    return LAeq_3oct


signal = signal_3oct()
signal_db = np.array(signal['db'])
signal_freq = signal['fr']

LAeq_3oct(signal_db, signal_freq)