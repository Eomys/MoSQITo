# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 00:49:39 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
#from  mosqito.utils.load import load
#from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum

def max_level_3oct(spectrum_signal_samples, freq):
    """Return the maximum value of the frequency bands you choose. Each one is calculated with the levels (dB)
    of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each column is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the max.

    Outputs
    -------
    max_level_3oct : numpy.ndarray
        the maximum values of each frequency band.
    """
    # Empty array to keep the levels (dB) of each one of the samples of a specific frequency band.
    main_freq = np.zeros(spectrum_signal_samples.shape[1])
    # Empty array to store the maximum values of each frequency band.
    max_level_3oct = np.zeros(freq.shape[0])
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]):
        # Save the values of a frequency band.
        for j in range(spectrum_signal_samples.shape[1]):
            main_freq[j] = spectrum_signal_samples[i,j]
        # Calculate the maximum with the values.
        max_level_3oct[i] = max(main_freq)

    return max_level_3oct


#if __name__ == "__main__":
    
    sig, fs = load(True,r"Programas_y_repositorios\MoSQITo\tests\input\1KHZ60DB.WAV", calib=1)

    spectrum_signal_samples = noct_spectrum(sig,fs)[0]
    freq = np.array(noct_spectrum(sig,fs)[1])

    max = max_level_3oct(spectrum_signal_samples,freq)
    print(max)
    pass