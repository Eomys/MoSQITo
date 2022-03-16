# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 16:57:37 2022

@author: wantysal
"""

import numpy as np
from numpy.fft import fft

# local function import
from mosqito.utils.conversion import amp2db


def spectrum(signal,fs,window='hanning',db=True):
    """
    

    Parameters
    ----------
    signal : np.array
        time signal (n blocks x time)
    fs : integer
        sampling frequency
    db : boolean, optional
        indicates if the spectrum is in dB values. The default is True.

    Returns
    -------
    spectrum : np.array
        spectrum (n blocks x frequency)
    freq_axis : np.array
        frequency axis corresponding to the spectrum

    """

    # single time signal
    if len(signal.shape)==1:
        n = len(signal)
        if window == 'hanning':
            window = np.hanning(n)
        elif window == 'blackman':
            window = np.blackman(n)
        window = window / np.sum(window)
    
        # Creation of the spectrum by FFT
        spectrum = fft(signal * window)[0:n//2] * 1.42
        freq_axis = np.arange(0, n//2, 1) * (fs / n)
    
        if db == True:
            # Conversion into dB level
            module = np.abs(spectrum)
            spectrum = amp2db(module, ref=0.00002)    

    # n time signals
    elif len(signal.shape)>1:
        n = signal.shape[1]
        if window == 'hanning':
            window = np.hanning(n)
        elif window == 'blackman':
            window = np.blackman(n)
        window = window / np.sum(window)

        # Creation of the spectrum by FFT
        spectrum = fft(signal * window)[:,0:n//2] * 1.42
        freq_axis = np.tile(np.arange(0, int(n / 2), 1) * (fs / n), (signal.shape[0],1))

        if db == True:
            # Conversion into dB level
            module = np.abs(spectrum)
            spectrum = amp2db(module, ref=0.00002)
    
    return spectrum, freq_axis