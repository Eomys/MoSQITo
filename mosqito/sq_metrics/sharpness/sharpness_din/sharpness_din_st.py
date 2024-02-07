# -*- coding: utf-8 -*-

# Local imports
from mosqito.sq_metrics import loudness_zwst
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import sharpness_din_from_loudness


def sharpness_din_st(signal, fs, weighting="din", field_type="free"):
    """Acoustic sharpness calculation according to different methods:
        Aures, Von Bismarck, DIN 45692, Fastl

    Parameters:
    ----------
    signal: numpy.array
        A time signal in [Pa], dim (nperseg, nseg)
    fs: integer
        Sampling frequency
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse").

    Outputs
    ------
    S : float
        Sharpness value, dim (nseg)

    """

    if fs < 48000:
        print("[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
             )
        from scipy.signal import resample
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000

    # Compute loudness
    N, N_specific, _ = loudness_zwst(signal, fs, field_type=field_type)

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting)

    return S
