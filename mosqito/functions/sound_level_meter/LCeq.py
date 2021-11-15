# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:37:08 2021

@author: Igarciac117 
"""

import numpy as np

# Local imports
from Leq import Leq

# pink_noise 40.0 dB
spectrum_pink = np.array(
    [
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
        40.0,
    ]
)

freq = np.array(
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

def C_weighting(spectrum, freq_axis):

    # Ponderation coefficients from the standard
    C_standard = np.array(
        [
            -14.3,
            -11.2,
            -8.5,
            -6.2,
            -4.4,
            -3.0,
            -2.0,
            -1.3,
            -0.8,
            -0.5,
            -0.3,
            -0.2,
            -0.1,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0,
            0.0,
            -0.1,
            -0.2,
            -0.3,
            -0.5,
            -0.8,
            -1.3,
            -2.0,
            -3.0,
            -4.4,
            -6.2,
            -8.5,
            -11.2,
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

    C_pond = np.interp(freq_axis, freq_standard, C_standard)

    spectrum_dBC = np.zeros(spectrum.shape)
    for i in range(spectrum.shape[0]):
        spectrum_dBC[i] = spectrum[i] + C_pond[i]

    return spectrum_dBC

def LCeq (spectrum,freq):
    spectrum_C = C_weighting(spectrum,freq)
    LCeq = Leq(spectrum_C)

    print(spectrum_C)
    print(LCeq)
    print("hola LCeq")

    return LCeq

LCeq(spectrum_pink, freq)