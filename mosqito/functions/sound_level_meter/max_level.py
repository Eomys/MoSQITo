# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math

# Local imports
from mosqito.functions.shared.load import load
from mosqito.methods.Audio.compute_level import compute_level
from mosqito.functions.oct3filter.calc_third_octave_levels import calc_third_octave_levels

def max_level(db_samples_signal):
    """Calculate the maximum value of the series of levels (dB) collected over time (samples)

    Parameters
    ----------
    db_samples_signal : numpy.ndarray
        array in which each line is the db values of a sample.

    Outputs
    -------
    max_level : numpy.ndarray
        return the maximum value of the samples.
    """
    # Save the maximum level.
    max_level = np.array(max(db_samples_signal))

    return max_level


if __name__ == "__main__":
    
    sig, fs = load(True, r"Programas_y_repositorios\MoSQITo\tests\input\1KHZ60DB.WAV", calib=1)

    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])

    # Creating a list of zeros of the size of the frequency bands (to keep the Leq values).
    sig_dB = np.zeros(spectrum_signal_samples.shape[1])
    # For each frequency band you perform the operation.
    for i in range(spectrum_signal_samples.shape[1]): 
        sum = 0
        # Performs the summation with all the values of the frequency band in the different samples.
        for j in range(spectrum_signal_samples.shape[0]):  
            # Operation: summation(10^(level(db)[i]/10))
            sum = sum + 10.0**(spectrum_signal_samples[j][i]/10.0)
        # Keep the Leq value in the box corresponding to the frequency band from which the calculation is being made.
        # Operation: 10 x log(base 10)[sum]
        sig_dB[i] = 10.0 * math.log((sum),10)
    

    max = max_level(sig_dB)
    print (max)
    
    pass