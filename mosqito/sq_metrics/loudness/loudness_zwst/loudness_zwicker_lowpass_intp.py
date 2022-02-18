# -*- coding: utf-8 -*-
"""
@date Created on Fri May 22 2020
@author martin_g for Eomys
"""

# Standard library imports
import math
import numpy as np


def loudness_zwicker_lowpass_intp(loudness, tau, sample_rate):
    """1st order low-pass with linear interpolation of signal for
    increased precision

    Parameters
    ----------
    loudness : numpy.ndarray
        Loudness vs. time
    tau : float
        Filter parameter
    sample_rate : int
        Louness signal sampling frequency

    Outputs
    -------
    filt_loudness : numpy.ndarray
        Filtered loudness
    """
    filt_loudness = np.zeros(np.shape(loudness))
    # Factor for virtual upsampling/inner iterations
    lp_iter = 24

    num_samples = np.shape(loudness)[0]
    a1 = math.exp(-1 / (sample_rate * lp_iter * tau))
    b0 = 1 - a1
    y1 = 0

    for i in range(num_samples):
        x0 = loudness[i]
        y1 = b0 * x0 + a1 * y1
        filt_loudness[i] = y1

        # Linear interpolation steps between current and next sample
        if i < num_samples - 1:
            xd = (loudness[i + 1] - x0) / lp_iter
            # Inner iterations/interpolation
            for ii in range(lp_iter):
                x0 += xd
                y1 = b0 * x0 + a1 * y1
    return filt_loudness
