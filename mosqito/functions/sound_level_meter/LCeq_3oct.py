# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 19:36:20 2023

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math

# Local imports
from spectrum2dBC import spectrum2dBC
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

def LCeq_3oct (data_all_signals, fs, f_min, f_max):
    """Calculate the LCeq of the frequency bands you choose, returns the calculated LCeq values for each band.
    Each one is calculated with the levels (dBC) of its band in the different samples.

    Parameters
    ----------
    data_all_signals : numpy.ndarray
        Array which each row corresponds to the data of a signal [Pa].
    fs : float
        Sampling frequency [Hz].
    fmax : float
        Max frequency band [Hz].
    fmin : float
        Min frequency band [Hz].

    Outputs
    -------
    LCeq_3oct : numpy.ndarray
        The LCeq values (dBC) for each frequency band.
    """
    # We initialize the array that stores the third octave values (in Pa) of the all signals ​​with the first signal.
    spectrum_all_signals_Pa = noct_spectrum(data_all_signals[0],fs,f_min,f_max)[0]
    # We initialize the center frequencies of the third octaves with the first signal.
    freq = noct_spectrum(data_all_signals[0],fs,f_min,f_max)[1]
    # We initialize the number of the signals.
    num_signals = data_all_signals.shape[0]
    # We initialize the number of frequency bands.
    num_bands = freq.shape[0]

    # Calculate the value of the third octave in Pa of each signal.
    for i in range(num_signals):
        # We skip the first signal because we have initialized with it.
        if i != 0:
            # We calculate and save the values ​​of the third octaves of the signals
            spectrum_all_signals_Pa = np.append(spectrum_all_signals_Pa,noct_spectrum(data_all_signals[i],fs,f_min,f_max)[0],axis=1)
    # We initialize the size of the array in which the data is stored.
    array_shape = spectrum_all_signals_Pa.shape

    # Empty array to store the values in dB of the third octave of the all signals.
    spectrum_all_signals_dB = np.zeros(array_shape)
    # For each frequency band you perform the operation.
    for i in range(num_bands):
        # Performs the conversion to dB with all the values of the frequency band in the different signals.
        for j in range(num_signals): 
            # Conversion Pa to dB.
            dB = amp2db(np.array(spectrum_all_signals_Pa[i][j]))
            # Save all values in dB of the third octave in another array.
            spectrum_all_signals_dB[i][j] = dB

    # Empty array to store the values in dBC of the third octave of the all signals.
    spectrum_all_signals_dBC = np.zeros(array_shape)
    # For each signal you perform the operation.
    for i in range(num_signals):
        # conversion dB to dBC of the all third octave values.
        dBC = spectrum2dBC(np.array(spectrum_all_signals_dB[:,i]), freq)
        # For each frequency band you perform the operation.
        for j in range(num_bands):
            # Save all values in dBC of the third octave in another array.
            spectrum_all_signals_dBC[j][i] = dBC[j]

    # Creating a list of zeros of the size of the frequency bands (to keep the LCeq values).
    LCeq_3oct = np.zeros(num_bands)
    # For each frequency band you perform the operation.
    for i in range(num_bands): 
        sum = 0
        # Performs the summation with all the values of the frequency band in the different signals.
        for j in range(num_signals):
            # Operation: summation(10^(level(db)[i]/10))
            sum = sum + 10.0**(spectrum_all_signals_dBC[i][j]/10.0)
        # Keep the LCeq value in the box corresponding to the frequency band from which the calculation is being made.
        # Operation: 10 x log(base 10)[1/number of samples x sum]
        LCeq_3oct[i] = 10.0 * math.log(((1/num_signals)*sum),10)

    return LCeq_3oct