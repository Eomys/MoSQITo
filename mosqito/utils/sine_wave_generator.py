# -*- coding: utf-8 -*-

import numpy as np
import math


def sine_wave_generator(fs, t, spl_value, freq):
    """
    Sine wave signal generation
    
    This function creates a sine wave signal given a frequency, duration, sampling rate and sound
    pressure level.

    Parameters
    ----------
    fs: int
        Sampling frequency in [Hz].
    t: int
        Signal duration in [s].
    spl_value: int
        Sound pressure level signal in [dB SPL].
    freq: int
        Sine wave frequency in [Hz].

    Returns
    -------
    signal: array_like
        Signal time values in [Pa]. 
    time: array_like
        Time axis in [s].
        
    Notes
    -----
    Signal to be used for ECMA-418-2 validation must have a sampling frequency of 48 kHz.
    """

    # "Peak" value in Pascals (amplitude)
    p_ref = 2e-5
    pressure_rms = p_ref * (10.00 ** (spl_value / 20.00))

    # Sample range
    # samples = np.linspace(0, t, int(fs * t), endpoint=False)
    time = np.arange(0, t, 1 / fs)

    # Theta lets you specify the sine wave value at time 0
    theta = 0

    # Amplitude of the signal
    amplitude = np.sqrt(2) * pressure_rms

    # Signal calculation
    signal = np.array(amplitude * np.sin((2.00 * math.pi * freq * time) + theta))

    return signal, time
