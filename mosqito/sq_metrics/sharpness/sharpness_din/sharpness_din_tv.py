# -*- coding: utf-8 -*-

# External import
import numpy as np

# Local imports
from mosqito.sq_metrics import loudness_zwtv
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import sharpness_din_from_loudness


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
    if fs < 48000:
        print("[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
             )
        from scipy.signal import resample
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000

    if skip == 0:
        print("[Warning] when computing sharpness from time-varying loudness, a transient effect appears on the first points. To cut it, use 'skip='")

    # Compute loudness
    N, N_specific, _, time_axis = loudness_zwtv(signal, fs)

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(
        N, N_specific, weighting=weighting, skip=0)

    # Cut transient effect
    cut_index = np.argmin(np.abs(time_axis - skip))

    return S[cut_index:], time_axis[cut_index:]
