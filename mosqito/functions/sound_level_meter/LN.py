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

def LN(db_samples_signal):
    """Calculate the percentile you want to study from a series of levels (dB) collected over time (samples)  

    Parameters
    ----------
    db_samples_signal : numpy.ndarray
        array in which each line is the db values of a sample.

    Outputs
    -------
    percentiles : numpy.ndarray
        calculated values ordered from lowest to highest percentile.
    """
    print('percentiles using interpolation = ', "linear")
    # Calculate the percentiles with the values. "q" of np.percentile = 100 - N (N of LN).
    L90 = np.percentile(db_samples_signal, 10,interpolation='linear') 
    L50 = np.percentile(db_samples_signal, 50,interpolation='linear') 
    L25 = np.percentile(db_samples_signal, 75,interpolation='linear')
    # Save the calculated percentile values.
    percentiles = np.array([L25,L50,L90])

    return percentiles


if __name__ == "__main__":
    
    sig, fs = load(True, r"Programas_y_repositorios\MoSQITo\tests\input\Test signal 3 (1 kHz 60 dB).wav", calib=1)
    sig_dB = np.array(sig)

    #Lp = 20 log10 (p/p0)
    for i in range(sig_dB.shape[0]):
        if sig_dB[i] <= 0.0:
            sig_dB[i] = 0
        else:
            sig_dB[i] = 20.0 * math.log((sig[i]/0.00002),10)
        
    percentile = LN(sig_dB)
    print(percentile)
    
    pass