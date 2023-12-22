# -*- coding: utf-8 -*-

from numpy import tile, hanning, blackman, concatenate, arange, abs
from numpy.fft import fft

# local function import
from mosqito.utils import amp2db


def comp_spectrum(signal,fs, nfft='default', window='hanning', one_sided=True, db=True):
    """
    Compute one-sided spectrum from a time signal in Pa.

    Parameters
    ----------
    signal : array
        A time signal (nperseg x nseg).
    fs : integer
        Sampling frequency.
    db : boolean, optional
        Indicates if the spectrum is in dB values. Default is True.

    Returns
    -------
    spectrum : array
        Spectrum (freq_axis x nseg).
    freq_axis : array
        Frequency axis.
        
    See also
    --------
    noct_synthesis : Conversion of a spectrum to n-th octave band levels
    noct_spectrum : N-th octave band spectrum computation from a time signal
    spectrum2dBA : Conversion of a spectrum from dB to dBA
        
    Examples
    --------
    .. plot::
       :include-source:
       
        >>> from mosqito.sound_level_meter import comp_spectrum
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fs=48000
        >>> d=0.2
        >>> dB=60
        >>> time = np.arange(0, d, 1/fs)
        >>> f = 1000
        >>> stimulus = 1 + 0.5*np.sin(2 * np.pi * f * time) + 0.1*np.sin(20 * np.pi * f * time)
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> spec_db, freq_axis = comp_spectrum(stimulus, fs, db=True)
        >>> plt.step(freq_axis, spec_db)
        >>> plt.xlabel("Center frequency [Hz]")
        >>> plt.ylabel("Amplitude [dB]")
    """
    if len(signal.shape)>1:
        nseg = signal.shape[1]
    else:
        nseg = 1
    
    # Number of points for the fft
    if nfft == 'default':
        if len(signal.shape) == 1:
            nfft = len(signal)
        else :
            nfft = signal.shape[0]

    # Window definition
    if window == 'hanning':
        window = hanning(nfft)
    elif window == 'blackman':
        window = blackman(nfft)
        
    # Amplitude correction
    window = window / sum(window)
    
    if len(signal.shape)>1:
        window = tile(window,(nseg,1)).T
    
    # Creation of the spectrum by FFT
    if one_sided == True:
        spectrum = fft(signal * window, n=nfft, axis=0)[0:nfft//2] * 1.42
        freq_axis = arange(1, nfft//2+1, 1) * (fs / nfft)
    else:
        spectrum = fft(signal * window, n=nfft, axis=0) * 1.42
        freq_axis = concatenate((arange(1, nfft//2+1, 1) * (fs / nfft), arange(nfft//2+1, 1, -1) * (fs / nfft)))

    if db == True:
        # Conversion into dB level
        module = abs(spectrum)
        spectrum = amp2db(module, ref=0.00002)
    
    return spectrum, freq_axis
