# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:00:50 2020

@author: wantysal
"""

# Standard library import
import numpy as np

# Local imports
from mosqito.functions.loudness_zwicker.comp_loudness import comp_loudness
from mosqito.functions.sharpness.sharpness_aures import comp_sharpness_aures
from mosqito.functions.sharpness.sharpness_din import comp_sharpness_din
from mosqito.functions.sharpness.sharpness_bismarck import comp_sharpness_bismarck
from mosqito.functions.sharpness.sharpness_fastl import comp_sharpness_fastl


def comp_sharpness(is_stationary, signal, fs, method="din", skip=0):
    """Acoustic sharpness calculation according to different methods:
        Aures, Von Bismarck, DIN 45692, Fastl

    Parameters:
    ----------
    is_stationary: boolean
        True if the signal is stationary, false if it is time varying
    signal: numpy.array
        time history values
    fs: integer
        sampling frequency
    method: string
        'din' by default,'aures', 'bismarck','fastl'
    skip : float
        number of second to be cut at the beginning of the analysis

    Outputs
    ------
    S : float
    sharpness value

    """

    if (
        method != "din"
        and method != "aures"
        and method != "fastl"
        and method != "bismarck"
    ):
        raise ValueError("ERROR: method must be 'din', 'aures', 'bismarck', 'fastl'")

    loudness = comp_loudness(is_stationary, signal, fs)

    if method == "din":
        S = comp_sharpness_din(
            loudness["values"], loudness["specific values"], is_stationary
        )

    elif method == "aures":
        S = comp_sharpness_aures(
            loudness["values"], loudness["specific values"], is_stationary
        )

    elif method == "bismarck":
        S = comp_sharpness_bismarck(
            loudness["values"], loudness["specific values"], is_stationary
        )

    elif method == "fastl":
        S = comp_sharpness_fastl(
            loudness["values"], loudness["specific values"], is_stationary
        )

    if is_stationary == False:
        # Cut transient effect
        time = np.linspace(0, len(signal) / fs, len(S))
        cut_index = np.argmin(np.abs(time - skip))
        S = S[cut_index:]

    output = {"name": "sharpness", "method": method, "values": S, "skip": skip}

    return output
