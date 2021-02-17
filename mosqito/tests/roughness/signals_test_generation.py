# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:17:27 2020

@author: wantysal
"""
# Standard library import
import numpy as np
from scipy.io.wavfile import write


def signal_test(fc, fmod, mdepth, fs, d, dB):
    """Creation of stationary amplitude modulated signals for the roughness
    validation procedure (signal created according to equation 1 in
    "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997.

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer
        modulation frequency
    mdepth: float
        modulation depth
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    """

    # time axis definition
    dt = 1 / fs
    time = np.arange(0, d, dt)

    signal = (
        0.5
        * (1 + mdepth * (np.sin(2 * np.pi * fmod * time)))
        * np.sin(2 * np.pi * fc * time)
    )
    rms = np.sqrt(np.mean(np.power(signal, 2)))
    ampl = 0.00002 * np.power(10, dB / 20) / rms
    signal = signal * ampl

    return signal


def wav_test(fc, fmod, mdepth, fs, d, dB, folder):
    """Creation of .wav file of stationary amplitude modulated signals for the roughness
    validation procedure (signal created according to equation 1 in
    "Psychoacoustical roughness:implementation of an optimized model"
    by Daniel and Weber in 1997.

    Parameters
    ----------
    fc: integer
        carrier frequency
    fmod: integer or numpy.array
        modulation frequency
    mdepth: float
        modulation depth
    fs: integer
        sampling frequency
    d: float
        signal duration [s]
    dB: integer
        SPL dB level of the carrier signal
    folder: string
        path of the folder where to store the file
    """

    values = test_signal(fc, fmod, mdepth, fs, d, dB)
    values = values / (2 * 2 ** 0.5)
    values = values.astype(np.int16)
    write(
        folder + "\Test_signal_fc" + str(fc) + "_fmod" + str(fmod) + ".wav", fs, values
    )
