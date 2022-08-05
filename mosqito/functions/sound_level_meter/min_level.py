# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math

# Local imports
#from  mosqito.utils.load import load
#from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
#from mosqito.methods.Audio.compute_level import compute_level

def min_level(db_samples_signal):
    """Calculate the minimum value of the series of levels (dB) collected over time (samples)

    Parameters
    ----------
    db_samples_signal : numpy.ndarray
        array in which each line is the db values of a sample.

    Outputs
    -------
    minimum : numpy.ndarray
        return the minimum value of the samples.
    """
    # Save the minimum level.
    min_level = min(db_samples_signal)

    return min_level

#if __name__ == "__main__":
    
    sig, fs = load(True, r"Programas_y_repositorios\MoSQITo\tests\input\1KHZ60DB.WAV", calib=1)
    
    spectrum_signal_samples = noct_spectrum(sig,fs)[0]
    freq = np.array(noct_spectrum(sig,fs)[1])

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
        
    min = min_level(sig_dB)
    print (min)
    
    pass