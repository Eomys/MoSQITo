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


def LN_3oct(spectrum_all_signals, freq):
    """Calculate the percentiles of the frequency bands you choose, returns the results for each frequency band.
    Each one is calculated with the levels (dB) of its band in the different samples.

    Parameters
    ----------
    spectrum_all_signals : numpy.ndarray
        Array which each column is the third octave band spectrum of each signal (Pa).
    freq : numpy.ndarray
        Corresponding preferred third octave band center frequencies.

    Outputs
    -------
    percentiles : numpy.ndarray
        The values in dB of L90, L50 and L25 for each third of an octave.
    """
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
            dB = amp2db(spectrum_all_signals[i][j])
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

    LN = LN_3oct(spectrum_all_signals,freq)
    print(LN)
    pass