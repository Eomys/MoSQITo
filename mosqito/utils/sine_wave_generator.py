# -*- coding: utf-8 -*-

from numpy import array, arange, sin, sqrt, pi


def sine_wave_generator(fs, d, freq, spl_level):
    """
    Sine wave signal generation
    
    This function creates a sine wave signal given a sampling rate, duration,
    frequency and sound pressure level.

    Parameters
    ----------
    fs: int
        Sampling frequency in [Hz].
    d: int
        Signal duration in [s].
    freq: int
        Sine wave frequency in [Hz].
    spl_level: int
        Sound pressure level signal in [dB SPL].
        
    Returns
    -------
    signal: array_like
        Signal time values in [Pa]. 
    time: array_like
        Time axis in [s].
        
    Warning
    -------
    spl_level must be provided in dB, ref=2e-5 Pa.
        
    Notes
    -----
    Signal to be used for ECMA-418-2 validation must have a sampling frequency of 48 kHz.
    
    Examples
    --------
    .. plot::
       :include-source:
       
        >>> from mosqito.utils import sine_wave_generator
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> fs = 48000     
        >>> duration = 1  
        >>> freq = 10    
        >>> dB = 60      
        >>> signal, time = sine_wave_generator(fs, duration, freq, dB)
        >>> plt.plot(time, signal)
        >>> plt.xlabel("Time axis [s]")
        >>> plt.ylabel("Amplitude signal [Pa]")    
    """

    # "Peak" value in Pascals (amplitude)
    p_ref = 2e-5
    pressure_rms = p_ref * (10.00 ** (spl_level / 20.00))

    # Sample range
    # samples = linspace(0, t, int(fs * t), endpoint=False)
    time = arange(0, d, 1 / fs)

    # Theta lets you specify the sine wave value at time 0
    theta = 0

    # Amplitude of the signal
    amplitude = sqrt(2) * pressure_rms

    # Signal calculation
    signal = array(amplitude * sin((2.00 * pi * freq * time) + theta))

    return signal, time
