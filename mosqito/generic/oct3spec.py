# -*- coding: utf-8 -*-
"""
@date Created on Fri Mar 13 2020
@author martin_g for Eomys
"""

import math
import numpy as np
from scipy import signal
from mosqito.generic.oct3level import oct3level


def oct3spec(sig, fs, fc_min=20, fc_max=20000):
    """Calculate third-octave band spectrum

    Calculate the rms level of the signa "sig" sampled at freqency "fs"
    for each third octave band between "fc_min" and "fc_max". 

    Parameters
    ----------
    sig : numpy.ndarray
        time signal [Any unit]
    fs : float
        Sampling frequency [Hz]
    fc_min : float
        Filter center frequency of the lowest 1/3 oct. band [Hz]
    fc_max : float
        Filter center frequency of the highest 1/3 oct. band [Hz]

    Outputs
    -------
    spec : numpy.ndarray
        Third octave band spectrum of signal sig [Any unit, rms]
    fpref : numpy.ndarray
        Corresponding preferred third octave band center frequencies
    """

    # TODO: control that fc_min and fc_max are in the right range
    # TODO: smarter management of the frequencies by using the ANSI
    #       definitions (with base 10 and base 2 options)

    # Définition of the range of preferred filter center frequency
    fpref = np.array(
        [
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
    fexact = np.array(
        [
            20,
            25.119,
            31.623,
            39.811,
            50.119,
            63.096,
            79.433,
            100,
            125.89,
            158.49,
            199.53,
            251.19,
            316.23,
            398.11,
            501.19,
            630.96,
            794.33,
            1000,
            1258.9,
            1584.9,
            1995.3,
            2511.9,
            3162.3,
            3981.1,
            5011.9,
            6309.6,
            7943,
            10000,
            12589,
            15849,
            19953,
        ]
    )
    fexact = fexact[fpref >= fc_min]
    fpref = fpref[fpref >= fc_min]
    fexact = fexact[fpref <= fc_max]
    fpref = fpref[fpref <= fc_max]

    # Calculation of the rms level of the signal in each band
    spec = np.zeros((len(fexact), 1))
    i = 0
    for fc in fexact:
        spec[i] = oct3level(sig, fs, fc)
        i += 1

    return spec, fpref
