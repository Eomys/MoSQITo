# -*- coding: utf-8 -*-
"""
Created on Wen Dic 1 18:08:08 2021

@author: Igarciac117 
"""

# Third party imports
import numpy as np

#Local imports. THIS IS NOT PART OF THE PROGRAM------------------------------------------------------------------------------------
from signal_time import signal_time

def max_level(db_samples_signal):
    """Calculate the maximum value of the series of levels (dB) collected over time (samples)

    Parameters
    ----------
    db_samples_signal : numpy.ndarray
        array in which each line is the db values of a sample.

    Outputs
    -------
    maximum : numpy.ndarray
        return the maximum value of the samples.
    """
    # Save the maximum level.
    max_level = np.array(max(db_samples_signal))

# this is not part of the program----------------------------------------------------------------------------------------
    print(max_level)
#------------------------------------------------------------------------------------------------------------------------

    return max_level

max_level(signal_time())