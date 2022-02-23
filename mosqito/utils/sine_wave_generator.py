# -*- coding: utf-8 -*-

import numpy as np
import math


def sine_wave_generator(fs, t, spl_value, freq):
    """It creates a sine wave signal given some input parameters like frequency, duration, sampling rate or sound
    pressure level.

    Parameters
    ----------
    fs: int
        'Hz', sampling frequency.
    t: int
        's', signal duration.
    spl_value: int
        'dB SPL', signal sound pressure level.
    freq: int
        'Hz', sine wave frequency.

    Returns
    -------
    signal: numpy.array
        'Pa', time signal values. For ECMA-418-2 the sampling frequency of the signal must be 48000 Hz.
    time: numpy.array
        Time scale arranged in a numpy array.
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
