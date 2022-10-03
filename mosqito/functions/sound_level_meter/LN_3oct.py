# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 00:45:30 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from  mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db


def LN_3oct(data_all_signals, fs, f_min, f_max):
    """Calculate the percentiles of the frequency bands you choose, returns the results for each frequency band.
    Each one is calculated with the levels (dB) of its band in the different samples.

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
    LN_3oct : numpy.ndarray
        The values in dB of L90, L50 and L25 for each third of an octave.
    """
    # We initialize the array that stores the third octave values of the all signals ​​with the first signal.
    spectrum_all_signals = noct_spectrum(data_all_signals[0],fs,f_min,f_max)[0]
    # We initialize the center frequencies of the third octaves with the first signal.
    freq = noct_spectrum(data_all_signals[0],fs,f_min,f_max)[1]
    # Calculate the value of the third octave of each signal.
    for i in range(data_all_signals.shape[0]):
        # We skip the first signal because we have initialized with it.
        if i != 0:
            # We calculate and save the values ​​of the third octaves of the signals
            spectrum_all_signals = np.append(spectrum_all_signals,noct_spectrum(data_all_signals[i],fs,f_min,f_max)[0],axis=1)
    print(spectrum_all_signals)
    print(spectrum_all_signals.shape[0])
    print(spectrum_all_signals.shape[1])

    # Empty array to store the values in dB of the third octave whose percentiles values are going to be calculated.
    main_freq_dB = np.zeros(spectrum_all_signals.shape[1])
    # Empty array to store the L90 values of each frequency band.
    percentile_L90 = np.zeros(freq.shape[0])
    # Empty array to store the L50 values of each frequency band.
    percentile_L50 = np.zeros(freq.shape[0])
    # Empty array to store the L25 values of each frequency band.
    percentile_L25 = np.zeros(freq.shape[0])
    print('percentiles using interpolation = ', "linear")
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]):
        # Performs the conversion to dB with all the values of the frequency band in the different signals.
        for j in range(spectrum_all_signals.shape[1]): 
            # Conversion Pa to dB.
            dB = amp2db(np.array(spectrum_all_signals[i][j]))
            # Save all values in dB of the third octave in another array.
            main_freq_dB[j] = dB
        # Calculate and keep the percentiles with the values. "q" of np.percentile = 100 - N (N of LN).
        percentile_L90[i] = np.percentile(main_freq_dB, 10,interpolation='linear')
        percentile_L50[i] = np.percentile(main_freq_dB, 50,interpolation='linear')
        percentile_L25[i] = np.percentile(main_freq_dB, 75,interpolation='linear')
    print("The values of L90, L50 and L25 of the thirds octaves")
    #Each row is the values of L90, L50 and L25 of its corresponding third octave.
    LN_3oct = np.stack((percentile_L90,percentile_L50,percentile_L25), axis=1)

    return LN_3oct


if __name__ == "__main__":

    sig_1, fs_1 = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    print(sig_1)
    print(fs_1)

    sig_2, fs_2 = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    sig_3, fs_3 = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")

    data_all_signals = np.stack((sig_1,sig_2,sig_3))
    print(data_all_signals)
    print(data_all_signals[0])

    f_min = 2000
    f_max =20000
    fs = fs_1

    print(data_all_signals.shape[0])
    LN = LN_3oct(data_all_signals,fs,f_min,f_max)
    print(LN)

    pass