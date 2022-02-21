# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 18:12:51 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from Leq_3oct import Leq_3oct
from mosqito.functions.shared.load import load
from mosqito.functions.oct3filter.calc_third_octave_levels import calc_third_octave_levels
from C_weighting import C_weighting

def LCeq_3oct (spectrum_signal_samples,freq):
    """Calculate the LCeq of the frequency bands you choose, returns the calculated LCeq values for each band.
    Each one is calculated with the levels (dBC) of its band in the different samples.

    Parameters
    ----------
    spectrum_signal_samples : numpy.ndarray
        array which each column is the dB values of the frequency bands in a sample.
    freq : numpy.ndarray
        array with the frequency bands you want to calculate the LCeq.

    Outputs
    -------
    LCeq_3oct : numpy.ndarray
        a list of the Leq values (dBC) for each frequency band.
    """
    # Empty list to keep the lists. Each list is the dBC values for each frequency band in a sample.
    signal_sample_C = []
    print("--------------------Lo que entra------------------------------")
    print(spectrum_signal_samples)
    print("--------------------Lo que entra en el cWEighfhhcj------------------------------")
    print(spectrum_signal_samples.T)
    # Take the columns of the array one by one and perform the function to transform the values in dB to dBC.
    for i in range(spectrum_signal_samples.shape[1]):
        # Save dBC values lists in the list "signal_sample_C".
        signal_sample_C.append(C_weighting(spectrum_signal_samples.T[i],freq))
    # Create an array in which each sample in dBC is a line of the array.
    spectrum_signal_samples_C_T = np.array(signal_sample_C)
    # You have to do the transpose of the matrix to be able to put each sample in a column
    spectrum_signal_samples_C = np.transpose(spectrum_signal_samples_C_T)
    print("--------------------spectrum_signal_traspuesta------------------------------")
    print(spectrum_signal_samples_C_T)
    print("-------------------Spectrum_signal_C_ENTRADA------------------------------")
    print(spectrum_signal_samples_C)
    print(spectrum_signal_samples_C.shape[0])
    print(spectrum_signal_samples_C.shape[1])

    # Calculate Leq of each frequency bands with the new dBC values.
    LCeq_3oct = Leq_3oct(spectrum_signal_samples_C, freq)

    return LCeq_3oct


if __name__ == "__main__":
    
    sig, fs = load(True,r"Programas_y_repositorios\MoSQITo\tests\input\1KHZ60DB.WAV", calib=1)

    spectrum_signal_samples = calc_third_octave_levels(sig,fs)[0]
    freq = np.array(calc_third_octave_levels(sig,fs)[1])

    LCeq = LCeq_3oct(spectrum_signal_samples,freq)
    print(LCeq)
    pass