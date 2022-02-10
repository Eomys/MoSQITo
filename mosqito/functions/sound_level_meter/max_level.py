# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np
import math

# Local imports
from mosqito.functions.shared.load import load
from mosqito.methods.Audio.compute_level import compute_level

def max_level(db_samples_signal):
    """Calculate the maximum value of the series of levels (dB) collected over time (samples)

    Parameters
    ----------
    db_samples_signal : numpy.ndarray
        array in which each line is the db values of a sample.

    Outputs
    -------
    max_level : numpy.ndarray
        return the maximum value of the samples.
    """
    # Save the maximum level.
    max_level = np.array(max(db_samples_signal))

    return max_level


if __name__ == "__main__":
    
    sig, fs = load(True, r"Programas_y_repositorios\MoSQITo\tests\input\Test signal 3 (1 kHz 60 dB).wav", calib=1)
    sig_dB = np.array(sig)

    #Lp = 20 log10 (p/p0)
    for i in range(sig_dB.shape[0]):
        if sig_dB[i] <= 0.0:
            sig_dB[i] = 0
        else:
            sig_dB[i] = 20.0 * math.log((sig[i]/0.00002),10)
        
    max = max_level(sig_dB)
    print (max)
    
    pass