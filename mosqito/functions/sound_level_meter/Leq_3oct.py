# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 20:23:42 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math

# Local imports
from mosqito.functions.shared.load import load
from mosqito.functions.oct3filter.calc_third_octave_levels import calc_third_octave_levels

def Leq_3oct(spectrum_signal_samples, freq):
    """Calculate the Leq of the frequency bands you choose, returns the calculated Leq values for each band.
    Each one is calculated with the levels (dB) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each line is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the Leq.

    Outputs
    -------
    Leq_freq : numpy.ndarray
        the Leq values (dB) for each frequency band.
    """
    # Creating a list of zeros of the size of the frequency bands (to keep the Leq values).
    Leq_3oct = np.zeros(freq.shape)
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]):
        sum = 0
        # Performs the summation with all the values of the frequency band in the different samples.
        for j in range(spectrum_signal_samples.shape[0]):  
            # Operation: summation(10^(level(db)[i]/10))
            sum = sum + 10.0**(spectrum_signal_samples[j,i]/10.0)
        # Keep the Leq value in the box corresponding to the frequency band from which the calculation is being made.
        # Operation: 10 x log(base 10)[1/number of samples x sum]
        Leq_3oct[i] = 10.0 * math.log(((1/spectrum_signal_samples.shape[0])*sum),10)

    return Leq_3oct


if __name__ == "__main__":
    
    sig, fs = load(True, r"Programas_y_repositorios\MoSQITo\tests\input\white_noise_200_2000_Hz_stationary.wav", calib=1)

    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])

    Leq = Leq_3oct(spectrum_signal_samples,freq)
    print(Leq)
    pass