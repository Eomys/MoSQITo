# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:00:50 2020

@author: wantysal
"""

# Standard library import
import numpy as np

# Local imports
from mosqito.sq_metrics import loudness_zwst
from mosqito.sq_metrics.sharpness.sharpness_din._sharpness_aures import (
    _comp_sharpness_aures,
)
from mosqito.sq_metrics.sharpness.sharpness_din._sharpness_din import (
    _comp_sharpness_din,
)
from mosqito.sq_metrics.sharpness.sharpness_din._sharpness_bismarck import (
    _comp_sharpness_bismarck,
)
from mosqito.sq_metrics.sharpness.sharpness_din._sharpness_fastl import (
    _comp_sharpness_fastl,
)


def sharpness_din(is_stationary, signal, fs, method="din", skip=0):
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

    N, N_specific, _ = loudness_zwst(signal, fs)

    if method == "din":
        S = _comp_sharpness_din(N, N_specific, is_stationary)

    elif method == "aures":
        S = _comp_sharpness_aures(N, N_specific, is_stationary)

    elif method == "bismarck":
        S = _comp_sharpness_bismarck(N, N_specific, is_stationary)

    elif method == "fastl":
        S = _comp_sharpness_fastl(N, N_specific, is_stationary)

    if is_stationary == False:
        # Cut transient effect
        time = np.linspace(0, len(signal) / fs, len(S))
        cut_index = np.argmin(np.abs(time - skip))
        S = S[cut_index:]

    return S
