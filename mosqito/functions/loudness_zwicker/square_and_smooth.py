# -*- coding: utf-8 -*-
"""
@date Created on Fri May 22 2020
@author martin_g for Eomys
"""

# Standard library imports
import numpy as np
from scipy import signal


def square_and_smooth(sig, center_freq, fs):
    """3rd order low-pass filtering (See ISO 532-1 section 6.3)

    Parameters
    ----------
    sig : numpy.ndarray
        time signal sampled at 48 kHz [pa]
    coeff : numpy.ndarray
        filter coeeficients
    gain : float
        filter gain

    Outputs
    -------
    signal_filt : numpy.ndarray
        filtered time signal
    """
    # Frequency dependent time constant
    if center_freq <= 1000:
        tau = 2 / (3 * center_freq)
    else:
        tau = 2 / (3 * 1000)
    # Squaring
    sig = sig ** 2
    # Three smoothing low-pass filters
    a1 = np.exp(-1 / (fs * tau))
    b0 = 1 - a1
    # zi = signal.lfilter_zi([b0], [1 -a1])
    for i in range(3):
        sig = signal.lfilter([b0], [1, -a1], sig)
    return sig
