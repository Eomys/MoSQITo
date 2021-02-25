# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 15:47:08 2020

@author: pc
"""

import numpy as np


def A_weighting(spectrum, freq_axis):
    """A_weighting dB ponderation of a spectrum according to CEI 61672:2014

    Third-octave spectrum are directly calculated, other are calculated
    using linear interpolation.

    Parameters
    ----------
    spectrum: numpy.array
              input spectrum
    fs: integer
        sampling frequency

    """

    # Ponderation coefficients from the standard
    A_standard = np.array(
        [
            -70.4,
            -63.4,
            -56.7,
            -50.5,
            -44.7,
            -39.4,
            -34.6,
            -30.2,
            -26.2,
            -22.5,
            -19.1,
            -16.1,
            -13.4,
            -10.9,
            -8.6,
            -6.6,
            -4.8,
            -3.2,
            -1.9,
            -0.8,
            0,
            0.6,
            1,
            1.2,
            1.3,
            1.2,
            1,
            0.5,
            -0.1,
            -1.1,
            -2.5,
            -4.3,
            -6.6,
            -9.3,
        ]
    )

    freq_standard = np.array(
        [
            10,
            12.5,
            16,
            20,
            25,
            31.5,
            40,
            50,
            63,
            80,
            100,
            125,
            160,
            200,
            250,
            315,
            400,
            500,
            630,
            800,
            1000,
            1250,
            1600,
            2000,
            2500,
            3150,
            4000,
            5000,
            6300,
            8000,
            10000,
            12500,
            16000,
            20000,
        ]
    )

    A_pond = np.interp(freq_axis, freq_standard, A_standard)

    spectrum_dBA = np.zeros(spectrum.shape)
    for i in range(spectrum.shape[0]):
        spectrum_dBA[i] = spectrum[i] + A_pond[i]

    return spectrum_dBA
