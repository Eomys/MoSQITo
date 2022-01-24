# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

#Local imports. THIS IS NOT PART OF THE PROGRAM------------------------------------------------------------------------------------
from signal_time import signal_time

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

#This is not part of the program ---------------------------------------------------------------------------------------------
    print('L90 = ',L90,', median = ',L50,' L25 = ',L25)
    print(percentiles)
#--------------------------------------------------------------------------------------------------------------------------------

    return percentiles

LN(signal_time())