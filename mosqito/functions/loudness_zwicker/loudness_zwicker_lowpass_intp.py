# -*- coding: utf-8 -*-
"""
@date Created on Fri May 22 2020
@author martin_g for Eomys
"""

# Standard library imports
import math
import numpy as np
#Needed for the loudness_zwicker_lowpass_intp_ea function
from scipy import signal

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
            # Must add a -1 because is repeating the twice the first value at the initial of the first for loop.
            for ii in range(lp_iter-1):
                x0 += xd
                y1 = b0 * x0 + a1 * y1
    return filt_loudness


def loudness_zwicker_lowpass_intp_ea(loudness, tau, sample_rate):
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

    delta = np.copy(loudness)
    delta = np.roll(delta,-1)
    delta [-1] = 0
    delta = (delta - loudness) /  lp_iter
    ui_delta = np.zeros(loudness.shape[0]*lp_iter).reshape(loudness.shape[0],lp_iter)
    ui_delta [:,0] = loudness  
    
    #Create the array complete of deltas to apply the filter.
    for i_in in np.arange(1, lp_iter):
        ui_delta [:,i_in] = delta + ui_delta [:,i_in-1]  
    
    # Rechape into a vector.
    ui_delta = ui_delta.reshape(lp_iter*num_samples)

    # Sustituir este bucle for por  scipy.signal.lfilter https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lfilter.html
    # ui_delta_filt = scipy.signal.lfilter (b0 , a0, ui_delta  )
    #filt_loudness = ui_delta_filt.reshape(loudness.shape[0],lp_iter).T[:,0]
    # Apply the filter.
    ui_delta = signal.lfilter([b0], [1,-a1], ui_delta, axis=- 1, zi=None)
    
    # Reshape again to recover the first col.
    ui_delta = ui_delta.reshape(loudness.shape[0],lp_iter)
    filt_loudness = ui_delta[:,0]
    return filt_loudness
