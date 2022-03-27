# -*- coding: utf-8 -*-

# Standard library import
import numpy as np

# Local imports
from mosqito.sq_metrics import loudness_zwst_perseg
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import (
    sharpness_din_from_loudness,
)


def sharpness_din_perseg(
    signal,
    fs,
    weighting="din",
    nperseg=4096,
    noverlap=None,
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
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    nperseg: int, optional
        Length of each segment. Defaults to 4096.
    noverlap: int, optional
        Number of points to overlap between segments.
        If None, noverlap = nperseg / 2. Defaults to None.
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
    N, N_specific, _, time_axis = loudness_zwst_perseg(
        signal, fs, nperseg=nperseg, noverlap=noverlap, field_type=field_type
    )

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting, skip=0)

    return S, time_axis
