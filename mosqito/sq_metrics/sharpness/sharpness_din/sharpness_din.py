# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:00:50 2020

@author: wantysal
"""

# Standard library import
import numpy as np

# Local imports
from mosqito.sq_metrics import loudness_zwst
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import (
    sharpness_din_from_loudness,
)
from mosqito.sq_metrics.sharpness.sharpness_din._sharpness_aures import (
    _comp_sharpness_aures,
)
from mosqito.sq_metrics.sharpness.sharpness_din._sharpness_bismarck import (
    _comp_sharpness_bismarck,
)
from mosqito.sq_metrics.sharpness.sharpness_din._sharpness_fastl import (
    _comp_sharpness_fastl,
)


def sharpness_din(
    signal, fs, method="zwst", weighting="din", field_type="free", skip=0
):
    """Acoustic sharpness calculation according to different methods:
        Aures, Von Bismarck, DIN 45692, Fastl

    Parameters:
    ----------
    signal: numpy.array
        time history values
    fs: integer
        sampling frequency
    method : string
        To specify the Loudness computation method
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse").
    skip : float
        number of second to be cut at the beginning of the analysis

    Outputs
    ------
    S : float
    sharpness value

    """

    is_stationary = True

    if (
        weighting != "din"
        and weighting != "aures"
        and weighting != "fastl"
        and weighting != "bismarck"
    ):
        raise ValueError("ERROR: weighting must be 'din', 'aures', 'bismarck', 'fastl'")

    if method == "zwst":
        N, N_specific, _ = loudness_zwst(signal, fs, field_type=field_type)
    elif method == "zwtv":
        pass
    else:
        raise ValueError("ERROR: method must be either 'zwst' or 'zwtv'")

    if weighting == "din":
        # S = _comp_sharpness_din(N, N_specific, is_stationary)
        S = sharpness_din_from_loudness(N, N_specific, weighting="din", skip=0)

    elif weighting == "aures":
        S = _comp_sharpness_aures(N, N_specific, is_stationary)

    elif weighting == "bismarck":
        S = _comp_sharpness_bismarck(N, N_specific, is_stationary)

    elif weighting == "fastl":
        S = _comp_sharpness_fastl(N, N_specific, is_stationary)

    if is_stationary == False:
        # Cut transient effect
        time = np.linspace(0, len(signal) / fs, len(S))
        cut_index = np.argmin(np.abs(time - skip))
        S = S[cut_index:]

    return S
