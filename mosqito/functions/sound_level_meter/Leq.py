# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 15:10:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math


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
        50.0,
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
        40.0,
        50.0,
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
        40.0,
        40.0,
        50.0,
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

def Leq(spectrum_signal_samples, freq):
    """You choose the frequencies you want to study, the Leq of each frequency is calculated independently 
    with their respective levels (dB) collected in each sample.  

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array in which each line is the db values of a sample.
    freq : numpy.ndarray
        array with the frequencies you want to calculate the Leq 

    Outputs
    -------
    Leq_freq : numpy.ndarray
        a list of the Leq values for each frequency
    """
    # Creating a list of zeros of the size of the frequencies (to put the values of Leq).
    Leq_freq = np.zeros(freq.shape)
    # For each frequency you perform the operation.
    for i in range(freq.shape[0]):
        sum = 0
        # Performs the summation with all the values of the frequency in the different samples.
        for j in range(spectrum_signal_samples.shape[0]):  
            # Operation: summation(10^(level(db)[i]/10))
            sum = sum + 10.0**(spectrum_signal_samples[j,i]/10.0)
        # save the Leq value in the box corresponding to the frequency from which the calculation is being made.
        # Operation: 10 x log(base 10)[1/number of samples x sum]
        Leq_freq[i] = 10.0 * math.log(((1/spectrum_signal_samples.shape[0])*sum),10)

    #THIS IS NOT PART OF THE FUNCTION----------------------------------------------------------------------------------------------
    print(spectrum_signal_samples)
    print(Leq_freq)
    print("hola Leq")
    #-------------------------------------------------------------------------------------------------------------------------------
    
    return Leq_freq

#Leq(pink_noise_signal, freq_standard)