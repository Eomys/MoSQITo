# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 00:45:30 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
#from  mosqito.utils.load import load
#from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum

def LN_3oct(spectrum_signal_samples, freq):
    """Calculate the percentiles of the frequency bands you choose, returns the results for each frequency band.
    Each one is calculated with the levels (dB) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each column is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the LN.

    Outputs
    -------
    percentile_L90 : numpy.ndarray
        the 90_ percentiles of each frequency band.
    """
    # Empty array to keep the levels (dB) of each one of the samples of a specific frequency band.  
    main_freq = np.zeros(spectrum_signal_samples.shape[1])
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
        for j in range(spectrum_signal_samples.shape[1]):
            main_freq[j] = spectrum_signal_samples[i,j]
        # Calculate the percentiles with the values. "q" of np.percentile = 100 - N (N of LN).
        L90 = np.percentile(main_freq, 10,interpolation='linear')
        L50 = np.percentile(main_freq, 50,interpolation='linear') 
        L25 = np.percentile(main_freq, 75,interpolation='linear')
        # Save in each array the values corresponding to its percentile. Each value of the array line belongs
        # to a frequency band.
        print(freq[i])
        print("---------------------------------------------------------------------------------")
        print("Percentile_90: ")
        percentile_L90[i] = L90
        print(L90)
        print("Percentile_50: ")
        percentile_L50[i] = L50
        print(L50)
        print("Percentile_25: ")
        percentile_L25[i] = L25
        print(L50)

    return percentile_L90


#if __name__ == "__main__":
    
    sig, fs = load(True, r"Programas_y_repositorios\MoSQITo\tests\input\1KHZ60DB.WAV", calib=1)

    spectrum_signal_samples = noct_spectrum(sig,fs)[0]
    freq = np.array(noct_spectrum(sig,fs)[1])

    LN = LN_3oct(spectrum_signal_samples,freq)
    print(LN)
    pass