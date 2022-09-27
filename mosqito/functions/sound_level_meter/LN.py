# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math

# Local imports
from mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

def LN(signal):
    """Calculate the percentile value of the series of levels (dB) of the one signal.  

    Parameters
    ----------
    signal : numpy.array
        time signal values

    Outputs
    -------
    percentiles : numpy.ndarray
        The values in dB of L90, L50 and L25 of the signal.
    """
    # Empty array to store the values in dB of the signal.
    dB_values = np.zeros(signal.shape[0])
    # Performs the conversion to dB with all the values of the signal.
    print(signal)
    print(signal.shape)
    for i in range(signal.shape[0]):
        # Conversion Pa to dB.
        dB = amp2db(np.array(signal[i]))
        # Save all values in dB of the third octave in another array.
        dB_values[i] = dB
    print('percentiles using interpolation = ', "linear")
    # Calculate the percentiles with the values. "q" of np.percentile = 100 - N (N of LN).
    L90 = np.percentile(dB_values, 10,interpolation='linear') 
    L50 = np.percentile(dB_values, 50,interpolation='linear') 
    L25 = np.percentile(dB_values, 75,interpolation='linear')
    print("The values of L90, L50 and L25 of the thirds octaves")
    # Save the calculated percentile values.
    percentiles = np.array([L90,L50,L25])

    return percentiles


if __name__ == "__main__":
    
    sig, fs = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    print(sig.shape)
    print(fs)

    signal = np.array(sig)

    percentiles = LN(signal)
    print(percentiles)
    
    pass