# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

# Local imports
from  mosqito.utils.load import load
from mosqito.sound_level_meter.noct_spectrum.noct_spectrum import noct_spectrum
from mosqito.utils.conversion import amp2db

def min_level(signal):
    """Calculate the minimum value of the series of levels (dB) of the one signal.

    Parameters
    ----------
    signal : numpy.array
        time signal values

    Outputs
    -------
    min_level : numpy.ndarray
        return the minimum value of the signal values.
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
    # Save the minimum level.
    min_level = np.array(min(dB_values))

    return min_level


if __name__ == "__main__":
    
    sig, fs = load(r"tests\input\Test signal 5 (pinknoise 60 dB).wav")
    print(sig.shape)
    print(fs)

    signal = np.array(sig)

    min = min_level(signal)
    print (min)
    
    pass