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

#THIS IS NOT A PART OF THE FUNCTION, it is a signal created by me to test if it works ------------------------------------------------
freq_standard = np.array(
        [
            10,
            12.5,
            16,
            20,
            25,
            31.5,
            40,
            50,
            63,
            80,
            100,
            125,
            160,
            200,
            250,
            315,
            400,
            500,
            630,
            800,
            1000,
            1250,
            1600,
            2000,
            2500,
            3150,
            4000,
            5000,
            6300,
            8000,
            10000,
            12500,
            16000,
            20000,
        ]
    )

# pink_noise 40.0 dB samples
spectrum_pink_first_sample = [
        10.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
    ]
spectrum_pink_second_sample = [
        20.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
    ]
spectrum_pink_third_sample = [
        30.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
    ]

# pink noise signal
pink_noise_samples = [spectrum_pink_first_sample, spectrum_pink_second_sample, spectrum_pink_third_sample]
pink_noise_signal = np.array(pink_noise_samples)
#-----------------------------------------------------------------------------------------------------------------------------------

def LAeq (spectrum_signal_samples,freq):
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
    LAeq = Leq_3oct(spectrum_signal_samples_A, freq)
    
    # THIS IS NOT PART OF THE PROGRAM-----------------------------------------------------------------------------------------
    #print(spectrum_signal_samples_A)
    print(LAeq)  
    print("hola LAeq")
    #-------------------------------------------------------------------------------------------------------------------------
    
    return LAeq

LAeq(pink_noise_signal, freq_standard)