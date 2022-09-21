# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 00:49:39 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

def max_level_3oct(spectrum_all_signals, freq):
    """Return the maximum value of the frequency bands you choose. Each one is calculated with the levels (dB)
    of its band in the different signals.

    Parameters
    ----------
    spectrum_all_signals : numpy.ndarray
        Array which each column is the third octave band spectrum of each signal (Pa).
    freq : numpy.ndarray
        Corresponding preferred third octave band center frequencies.

    Outputs
    -------
    max_level_3oct : numpy.ndarray
        The maximum values of each frequency band.
    """
    # Creating a list of zeros of the size of the frequency bands (to keep the maximum level values).
    max_level_3oct = np.zeros(freq.shape)
    # Empty array to store the values in dB of the third octave whose maximum value is going to be calculated.
    main_freq_dB = np.zeros(spectrum_all_signals.shape[1])
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]):
        # Performs the conversion to dB with all the values of the frequency band in the different signals.
        for j in range(spectrum_all_signals.shape[1]): 
            # Conversion Pa to dB.
            dB = amp2db(spectrum_all_signals[i][j])
            # Save all values in dB of the third octave in another array.
            main_freq_dB[j] = dB
        # Calculate and keep the maximum value found in the array. That value will be the maximum of the third of an octave.
        max_level_3oct[i] = max(main_freq_dB)
    
    return max_level_3oct


if __name__ == "__main__":
    
    sig, fs = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    print(sig)
    print(fs)

    f_min = 2000
    f_max =20000
    spectrum_signal_1 = noct_spectrum(sig,fs,f_min,f_max)[0]
    spectrum_signal_2 = noct_spectrum(sig,fs,f_min,f_max)[0]
    spectrum_signal_3 = noct_spectrum(sig,fs,f_min,f_max)[0]

    print(spectrum_signal_1)
    print(spectrum_signal_1.shape[0])
    print(spectrum_signal_1.shape[1])

    spectrum_all_signals = np.stack((spectrum_signal_1,spectrum_signal_2,spectrum_signal_3), axis=1)
    print(spectrum_all_signals)
    print(spectrum_all_signals.shape[0])
    print(spectrum_all_signals.shape[1])

    freq = np.array(noct_spectrum(sig,fs,2000,20000)[1])
    print(freq)
    print(freq.shape[0])

    max_level = max_level_3oct(spectrum_all_signals,freq)
    print(max_level)
    pass