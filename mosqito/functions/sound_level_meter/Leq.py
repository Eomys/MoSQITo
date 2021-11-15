# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 20:20:08 2021

@author: Igarciac
"""

import numpy as np
import math

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

def Leq(spectrum):
    Leq_exp = np.zeros(spectrum.shape)

    for i in range(spectrum.shape[0]):
        Leq_exp[i] = 10.0**(spectrum[i]/10.0)

    Leq_sum = (1/34)*sum(Leq_exp)
    Leq = 10 * (math.log (Leq_sum,10))

    print(spectrum)
    print(Leq_exp)
    print(Leq_sum)
    print(Leq)
    print("hola Leq")
    
    return Leq

#Leq(spectrum_Leq)