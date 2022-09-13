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
from mosqito.utils.conversion import amp2db

def Leq_3oct(spectrum_all_signals, freq):
    """Calculate the Leq of the frequency bands you choose, returns the calculated Leq values for each band.
    Each one is calculated with the levels (dB) of its band in the different signals.

    Parameters
    ----------
    spectrum_all_signals : numpy.ndarray
        Array which each column is the third octave band spectrum of each signal (Pa).
    freq : numpy.ndarray
        Corresponding preferred third octave band center frequencies.

    Outputs
    -------
    Leq_3oct : numpy.ndarray
        The Leq values (dB) for each frequency band.
    """
    # Creating a list of zeros of the size of the frequency bands (to keep the Leq values).
    Leq_3oct = np.zeros(freq.shape)
    # For each frequency band you perform the operation.
    for i in range(freq.shape[0]): 
        sum = 0
        # Performs the summation with all the values of the frequency band in the different signals.
        for j in range(spectrum_all_signals.shape[1]):
            #conversion Pa to dB
            dB = amp2db(spectrum_all_signals[i][j])
            # Operation: summation(10^(level(db)[i]/10))
            sum = sum + 10.0**(dB/10.0)
        # Keep the Leq value in the box corresponding to the frequency band from which the calculation is being made.
        # Operation: 10 x log(base 10)[1/number of samples x sum]
        Leq_3oct[i] = 10.0 * math.log(((1/spectrum_all_signals.shape[1])*sum),10)

    return Leq_3oct


if __name__ == "__main__":
    
    sig, fs = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    print(sig)
    print(fs)

    spectrum_signal_1 = noct_spectrum(sig,fs,2000,20000)[0]
    spectrum_signal_2 = noct_spectrum(sig,fs,2000,20000)[0]
    spectrum_signal_3 = noct_spectrum(sig,fs,2000,20000)[0]
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

    Leq = Leq_3oct(spectrum_all_signals,freq)
    print(Leq)
    pass