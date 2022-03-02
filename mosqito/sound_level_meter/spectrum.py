# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 16:57:37 2022

@author: wantysal
"""

import numpy as np
from numpy.fft import fft

# local function import
from mosqito.utils.conversion import amp2db


def spectrum(signal,fs,db=True):

    n = len(signal)
    window = np.hanning(n)
    window = window / np.sum(window)

    # Creation of the spectrum by FFT
    spectrum = fft(signal * window) * 1.42
    freq_axis = np.arange(0, int(n / 2), 1) * (fs / n)

    if db == True:
        # Conversion into dB level
        module = np.abs(spectrum)
        spectrum = amp2db(module, ref=0.00002)
    
    return spectrum, freq_axis