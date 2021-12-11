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

#-----------------------------------------------------------------------------------------------------------------------------------

def LN_3oct(spectrum_signal_samples, freq):
    """Calculate the percentiles of the frequency bands you choose, returns the results for each frequency band.
    Each one is calculated with the levels (dB) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each line is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the Leq.

    Outputs
    -------
    percentile_L90 : numpy.ndarray
        the 90_ percentiles of each frequency band.
    """
    # Empty array to keep the levels (dB) of each one of the samples of a specific frequency band.  
    main_freq = np.zeros(spectrum_signal_samples.shape[0])
    # Empty array to store the L90 values of each frequency band.
    percentile_L90 = np.zeros(freq.shape[0])
    # Empty array to store the L90 values of each frequency band.
    percentile_L50 = np.zeros(freq.shape[0])
    # Empty array to store the L90 values of each frequency band.
    percentile_L25 = np.zeros(freq.shape[0])
    print('percentiles using interpolation = ', "linear")
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]):
        # Save the values of a frequency band.
        for j in range(spectrum_signal_samples.shape[0]):
            main_freq[j] = spectrum_signal_samples[j,i]
            # Calculate the percentiles with the values. "q" of np.percentile = 100 - N (N of LN).
            L90 = np.percentile(main_freq, 10,interpolation='linear')
            L50 = np.percentile(main_freq, 50,interpolation='linear') 
            L25 = np.percentile(main_freq, 75,interpolation='linear')
        # Save in each array the values corresponding to its percentile. Each value of the array line belongs
        # to a frequency band.
        percentile_L90[i] = L90
        percentile_L50[i] = L50
        percentile_L25[i] = L25
# THIS IS NOT PART OF THE FUNCTION --------------------------------------------------------------------------------------    
    print(freq)
    print(percentile_L90)
#------------------------------------------------------------------------------------------------------------------------
    return percentile_L90

LN_3oct(pink_noise_signal,freq)