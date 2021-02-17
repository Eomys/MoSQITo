# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:31:09 2020

@author: wantysal
"""
# Standard library import
import numpy as np


def adaptlevel(signal, dBin, dBout):
    """ Scales a given signal to the demanded digital level in dB SPL [ref 2e-5] """

    # Calculate the factor to use for adapting the signal
    factor = np.power(10, (dBout - dBin) / 20)

    # Adapt the signal
    signal_scaled = signal * factor

    return signal_scaled
