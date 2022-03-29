# -*- coding: utf-8 -*-

# Local imports
from mosqito.sq_metrics import loudness_zwst_perseg
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_st_from_loudness import sharpness_din_st_from_loudness


def sharpness_din_perseg(signal, fs, weighting="din", nperseg=4096, noverlap=None, field_type="free"):
    """Acoustic sharpness calculation according to different methods
        (Aures, Von Bismarck, DIN 45692, Fastl) from a stationary signal.

    Parameters:
    ----------
    signal: numpy.array
        A time signal in [Pa].
    fs: integer
        Sampling frequency.
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

    Outputs
    ------
    S : float
        Sharpness value, size(nseg).

    """

    # Compute loudness
    N, N_specific, _, time_axis = loudness_zwst_perseg(
        signal, fs, nperseg=nperseg, noverlap=noverlap, field_type=field_type
    )

    # Compute sharpness from loudness
    S = sharpness_din_st_from_loudness(N, N_specific, weighting=weighting)

    return S, time_axis
