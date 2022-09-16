# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 18:07:36 2022

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from Leq_3oct import Leq_3oct
from mosqito.utils.conversion import spectrum2dBA
from  mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

#from mosqito.sq_metrics.loudness.loudness_zwtv._third_octave_levels import _third_octave_levels

def LAeq_3oct (spectrum_all_signals,freq):
    """Calculate the LAeq of the frequency bands you choose, returns the calculated LAeq values for each band.
    Each one is calculated with the levels (dBA) of its band in the different samples.

    Parameters
    ----------
    spectrum_all_signals : numpy.ndarray
        Array which each column is the third octave band spectrum of each signal (Pa).
    freq : numpy.ndarray
        Corresponding preferred third octave band center frequencies.

    Outputs
    -------
    LAeq_3oct : numpy.ndarray
        The LAeq values (dBA) for each frequency band.
    """
    # Creating a empty list to keep the signals in dBA values. 
    signal_sample_A = []
    # Take the columns of the array one by one and perform the function to transform the values in dB.
    for i in range(spectrum_all_signals.shape[1]):
        #conversion Pa to dB
        dB = amp2db(spectrum_all_signals[i][j])
        # Save dBA values lists in the list "signal_sample_A".
        signal_sample_A.append(spectrum2dBA(spectrum_all_signals.T[i],freq))
    # Create an array in which each sample in dBA is a line of the array.
    spectrum_all_signals_A_T = np.array(signal_sample_A)
    # You have to do the transpose of the array to be able to put each sample in a column
    spectrum_all_signals_A = np.transpose(spectrum_all_signals_A_T)
    # Calculate Leq of each frequency bands with the new dBA values.
    LAeq_3oct = Leq_3oct(spectrum_all_signals_A, freq)
    
    return LAeq_3oct


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
    #print(freq.shape[1])

    LAeq = LAeq_3oct(spectrum_all_signals,freq)
    print(LAeq)
    pass