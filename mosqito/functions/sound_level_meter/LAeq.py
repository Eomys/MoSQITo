# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:02:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from Leq import Leq
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
    """You choose the frequencies you want to study, the LAeq of each frequency is calculated independently 
    with their respective levels (dB) collected in each sample.  

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array in which each line is the db values of a sample.
    freq : numpy.ndarray
        array with the frequencies you want to calculate the LAeq 

    Outputs
    -------
    LAeq : numpy.ndarray
        a list of the Leq values for each frequency
    """
    # Empty array to save in each line the values in dBA of each sample 
    signal_sample_A = []
    # Take all the lines with values in dB and convert them to dBA. Save dBA lines to a new array. 
    for i in range(spectrum_signal_samples.shape[0]):
        signal_sample_A.append(A_weighting(spectrum_signal_samples[i],freq))
    spectrum_signal_samples_A = np.array(signal_sample_A)
    # Calculate the Leq of each frequency with the new dBA values. 
    LAeq = Leq(spectrum_signal_samples_A, freq)
    
    # THIS IS NOT PART OF THE PROGRAM-----------------------------------------------------------------------------------------
    #print(spectrum_signal_samples_A)
    print(LAeq)  
    print("hola LAeq")
    #-------------------------------------------------------------------------------------------------------------------------
    
    return LAeq

LAeq(pink_noise_signal, freq_standard)