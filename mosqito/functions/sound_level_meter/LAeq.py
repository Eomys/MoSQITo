# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 20:20:08 2021

@author: Igarciac
"""

import numpy as np

# Local imports
from Leq import Leq
from mosqito.functions.shared.A_weighting import A_weighting

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

def LAeq (spectrum,freq):
    spectrum_A = A_weighting(spectrum,freq)
    solution = Leq(spectrum_A)
    print(spectrum_A)
    print(solution)
    print("hola LAeq")

#LAeq(spectrum_pink, freq)