# -*- coding: utf-8 -*-

# Standard library import
import numpy as np

# Local imports
from mosqito.sq_metrics import loudness_zwst
from mosqito.sq_metrics import loudness_zwtv
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import (
    sharpness_din_from_loudness,
)


def sharpness_din(
    signal,
    fs,
    freqs=[],
    method="zwst",
    weighting="din",
    field_type="free",
    skip=0,
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
    time_axis: numpy.array
        The time axis array, size (Ntime,) or None

    """

    # Compute loudness
    if method == "zwst":
        N, N_specific, _ = loudness_zwst(signal, fs, field_type=field_type)
    elif method == "zwtv":
        if len(freqs) > 0:
            raise ValueError(
                "With a 1D spectrum as input, use stationary calculation, with a 2D spectrum use stationary per block calculation or reconstruct a time signal"
            )
        else:
            N, N_specific, _ = loudness_zwtv(signal, fs)
    else:
        raise ValueError("ERROR: method must be either 'zwst' or 'zwtv'")

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting, skip=0)

    return S
