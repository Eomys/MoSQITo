# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:00:03 2022

@author: wantysal
"""
# Standard library imports
import numpy as np
from scipy.signal import butter, freqz


def _n_oct_freq_filter(spectrum, fs, fc, alpha, n=3):
    """ n-th octave filtering in frequency domain

    Designs a digital 1/3-octave filter with center frequency fc for
    sampling frequency fs. 

    Parameters
    ----------
    spec : numpy.ndarray
        Frequency spectrum [complex]
    fs : float
        Sampling frequency [Hz]
    fc : float
        Filter exact center frequency [Hz]
    alpha : float
        Ratio of the upper and lower band-edge frequencies to the mid-band
        frequency
    N : int, optional
        Filter order. Default to 3

    Outputs
    -------
    level : float
        Rms level of sig in the third octave band centered on fc
    """

    # Check for Nyquist-Shannon criteria
    if fc > 0.88 * (fs / 2):
        raise ValueError(
            """ERROR: Design not possible. Filter center frequency shall
            verify: fc <= 0.88 * (fs / 2)"""
        )

    # Normalized cutoff frequencies
    w1 = fc / (fs / 2) / alpha
    w2 = fc / (fs / 2) * alpha

    # define filter coefficient
    b, a = butter(n, [w1, w2], "bandpass", analog=False)
    
    
    
    
    # filter signal
    if len(spectrum.shape)>1:
        level = []
        # go into frequency domain
        w, h = freqz(b, a, worN=spectrum.shape[1])
        for i in range(spectrum.shape[0]):
            spec_filt = spectrum[i,:] * h
            # Compute overall rms level
            level.append(np.sqrt(np.sum(np.abs(spec_filt) ** 2)))
        level = np.array(level)
    else:
        # go into frequency domain
        w, h = freqz(b, a, worN=len(spectrum))
        spec_filt = spectrum * h
        # Compute overall rms level
        level = np.sqrt(np.sum(np.abs(spec_filt) ** 2)) 
    
    return level




