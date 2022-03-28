# -*- coding: utf-8 -*-

import numpy as np
from numpy.fft import fft

# local function import
from mosqito.utils.conversion import amp2db


def spectrum(signal,fs, nfft='default',window='hanning',db=True):
    """
    Compute one-sided spectrum from a time signal in Pa.

    Parameters
    ----------
    signal : np.array
        A time signal [nperseg x nseg].
    fs : integer
        Sampling frequency.
    db : boolean, optional
        Indicates if the spectrum is in dB values. Default is True.

    Returns
    -------
    spectrum : np.array
        Spectrum [freq_axis x nseg].
    freq_axis : np.array
        Frequency axis.

    """
    if len(signal.shape)>1:
        nseg = signal.shape[1]
    
    # Number of points for the fft
    if nfft == 'default':
        if len(signal.shape) == 1:
            nfft = len(signal)
        else :
            nfft = signal.shape[0]

    # Window definition
    if window == 'hanning':
        window = np.hanning(nfft)
    elif window == 'blackman':
        window = np.blackman(nfft)
        
    # Amplitude correction
    window = window / np.sum(window)
    
    window = np.tile(window,(nseg,1)).T
    
    # Creation of the spectrum by FFT
    spectrum = fft(signal * window, axis=0)[0:nfft//2] * 1.42
    freq_axis = np.arange(0, nfft//2, 1) * (fs / nfft)

    if db == True:
        # Conversion into dB level
        module = np.abs(spectrum)
        spectrum = amp2db(module, ref=0.00002)
    
    return spectrum, freq_axis