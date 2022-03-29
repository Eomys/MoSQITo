# -*- coding: utf-8 -*-

# External import
import numpy as np

# Local imports
from mosqito.sq_metrics import loudness_zwtv
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_tv_from_loudness import sharpness_din_tv_from_loudness


def sharpness_din_tv(signal, fs, weighting="din", field_type="free", skip=0):
    """Acoustic sharpness calculation according to different methods
        (Aures, Von Bismarck, DIN 45692, Fastl) for a time varying signal.

    Parameters:
    ----------
    signal : numpy.array
        A time signal values [Pa], size (Ntime,) 
    fs : integer
        Sampling frequency.
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse").
    skip : float
        Number of second to be cut at the beginning of the analysis to skip the transient effect.

    Outputs
    ------
    S : float
        Sharpness value, size (Ntime,) .
    time_axis: numpy.array
        The time axis array, size (Ntime,) .

    """

    # Compute loudness
    N, N_specific, _, time_axis = loudness_zwtv(signal, fs)

    # Compute sharpness from loudness
    S = sharpness_din_tv_from_loudness(N, N_specific,time_axis, weighting=weighting, skip=0)
    
    # Cut transient effect
    cut_index = np.argmin(np.abs(time_axis - skip))

    return S[cut_index:], time_axis[cut_index:]