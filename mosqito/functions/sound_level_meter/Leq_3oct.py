# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 20:23:42 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math

# Local imports
from  mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum

def Leq_3oct(spectrum_signal_samples, freq):
    """Calculate the Leq of the frequency bands you choose, returns the calculated Leq values for each band.
    Each one is calculated with the levels (dB) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each column is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the Leq.

    Outputs
    -------
    Leq_3oct : numpy.ndarray
        the Leq values (dB) for each frequency band.
    """
    # Creating a list of zeros of the size of the frequency bands (to keep the Leq values).
    Leq_3oct = np.zeros(freq.shape)
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]): 
        sum = 0
        # Performs the summation with all the values of the frequency band in the different samples.
        for j in range(spectrum_signal_samples.shape[1]):  
            # Operation: summation(10^(level(db)[i]/10))
            sum = sum + 10.0**(spectrum_signal_samples[i][j]/10.0)
        # Keep the Leq value in the box corresponding to the frequency band from which the calculation is being made.
        # Operation: 10 x log(base 10)[1/number of samples x sum]
        Leq_3oct[i] = 10.0 * math.log(((1/spectrum_signal_samples.shape[1])*sum),10)

    return Leq_3oct


if __name__ == "__main__":
    
    sig, fs = load(r"tests\input\1KHZ60DB.WAV", True)

    spectrum_signal_samples = noct_spectrum(sig,fs)[0]
    freq = np.array(noct_spectrum(sig,fs)[1])
    print(sig)
    print(spectrum_signal_samples)
    print(spectrum_signal_samples.shape[0])
    print(spectrum_signal_samples.shape[1])


    Leq = Leq_3oct(spectrum_signal_samples,freq)
    print(Leq)
    pass