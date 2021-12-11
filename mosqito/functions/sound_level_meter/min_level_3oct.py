# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 15:10:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

#THIS IS NOT A PART OF THE FUNCTION, it is a signal created by me to test if it works ------------------------------------------------
# pink_noise 40.0 dB samples
spectrum_pink_first_sample = [
        1.0,
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
        50.0,
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
        1.0,
    ]

spectrum_pink_third_sample = [
        100.0,
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
        80.0,
    ]

spectrum_pink_4_sample = [
        100.0,
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
        80.0,
    ]

# pink noise signal
pink_noise_samples = [spectrum_pink_first_sample, spectrum_pink_second_sample, spectrum_pink_third_sample, spectrum_pink_4_sample]
pink_noise_signal = np.array(pink_noise_samples)

freq = np.array(
        [
            10,
            12.5,
            16,
            20,
            25,
            31.5,
            20,
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
#----------------------------------------------------------------------------------------------------------------------------

def min_level_3oct(spectrum_signal_samples, freq):
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
        the minimum values of each frequency band.
    """
    # Empty array to keep the levels (dB) of each one of the samples of a specific frequency band.
    main_freq = np.zeros(spectrum_signal_samples.shape[0])
    # Empty array to store the minimum values of each frequency band.
    min_level_3oct = np.zeros(freq.shape[0])
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]):
        # Save the values of a frequency band.
        for j in range(spectrum_signal_samples.shape[0]):
            main_freq[j] = spectrum_signal_samples[j,i]
        # Calculate the maximum with the values.
        min_level_3oct[i] = min(main_freq) 
#this is not part of the program --------------------------------------------------------------------------------------------------
        print(freq[i])
        print(min_level_3oct)
#-----------------------------------------------------------------------------------------------------------------------
    return min_level_3oct

min_level_3oct(pink_noise_signal,freq)