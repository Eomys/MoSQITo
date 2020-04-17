# -*- coding: utf-8 -*-
"""
@date Created on Fri Mar 13 2020
@author martin_g for Eomys
"""

import sys
import math
from scipy import signal
from mosqito.generic.oct3dsgn import oct3dsgn


def oct3level(sig, fs, fc):
    """Calculate rms level of a signal in the third octave band fc 

    Calculate the rms level of the signal "sig" in the third-octave
    band centered on frequency "fc". If "fc" is such that fc < fs/200,
    the signal is downsampled for better third-octave filter design.

    Parameters
    ----------
    sig : numpy.ndarray
        time signal [any unit]
    fs : float
        Sampling frequency [Hz]
    fc : float
        Filter exact center frequency [Hz]

    Outputs
    -------
    level : float
        rms level of sig in the third octave band centered on fc
    """

    """
    For meaningful design results, center frequency used should 
    preferably be higher than fs/200 (source ???). The signal is
    then downsampled if fc < fs/200. The procedure is inspired by 
    script GenerateFilters.m by Aaron Hastings, Herrick Labs, 
    Purdue University (version: 31 Oct 00)
    """

    # Check for Nyquist-Shannon criteria
    if fc > 0.88 * (fs / 2):
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc <= 0.88 * (fs / 2)"""
        )

    # Adjust sampling frequency to respect "fc > fs/200"
    i = 0
    while fs / (fc * 2 ** i) > 200:
        i += 1
    fs_sub = 100 * math.floor(fs / (2 ** i) / 100)
    # Generate the 1/3 oct. digital filter
    b, a = oct3dsgn(fc, fs_sub, n=3)
    # Downsample the signal
    if fs != fs_sub:
        sig = signal.decimate(sig, 2 ** i)
    # Filter the signal
    sig_filt = signal.lfilter(b, a, sig)
    # Calculate rms level
    level = math.sqrt(sum(sig_filt ** 2) / len(sig_filt))

    return level
