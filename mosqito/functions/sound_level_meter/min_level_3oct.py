# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 19:43:20 2023

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

def min_level_3oct(data_all_signals, fs, f_min, f_max):
    """Return the minimum value of the frequency bands you choose. Each one is calculated with the levels (dB)
    of its band in the different signals.

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
    min_level_3oct : numpy.ndarray
        The minimum values of each frequency band.
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

    # Creating a list of zeros of the size of the frequency bands (to keep the maximum level values).
    min_level_3oct = np.zeros(num_bands)
    # Empty array to store the values in dB of the third octave whose maximum value is going to be calculated.
    band_value_all_signals = np.zeros(num_signals)
    # For each frequency band you perform the operation.
    for i in range(num_bands):
        # Performs the conversion to dB with all the values of the frequency band in the different signals.
        for j in range(num_signals): 
            # Conversion Pa to dB.
            dB = amp2db(np.array(spectrum_all_signals_Pa[i][j]))
            # Save all values in dB of the third octave in another array.
            band_value_all_signals[j] = dB
        # Calculate and keep the maximum value found in the array. That value will be the maximum of the third of an octave.
        min_level_3oct[i] = min(band_value_all_signals)

    return min_level_3oct