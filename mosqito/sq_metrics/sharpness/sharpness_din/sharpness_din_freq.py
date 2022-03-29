# -*- coding: utf-8 -*-

import numpy as np
# Local imports
from mosqito.sq_metrics import loudness_zwst_freq
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_st_from_loudness import sharpness_din_st_from_loudness


def sharpness_din_freq(spectrum, freqs, weighting="din", field_type="free"):
    """Acoustic sharpness calculation according to different methods
      (Aures, Von Bismarck, DIN 45692, Fastl) from a complex spectrum.

    Parameters:
    ----------
    signal: numpy.array
        A complex spectrum.
    freqs: integer
        Frequency axis.
    method : string
        To specify the Loudness computation method
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse").

    Outputs
    ------
    S : float
        sharpness value
    time_axis: numpy.array
        The time axis array, size (Ntime,) or None

    """
    if spectrum.shape != freqs.shape :
        raise ValueError('Input spectrum and frequency axis must have the same shape')
    
    if np.iscomplexobj(np.array(spectrum)) == False:
        raise ValueError('Input spectrum must be complex !')

    # Compute loudness
    N, N_specific, _ = loudness_zwst_freq(spectrum,freqs, field_type=field_type)

    if len(spectrum.shape) > 1:
        raise ValueError("With a 2D spectrum use 'sharpness_din_perseg' calculation.")

    # Compute sharpness from loudness
    S = sharpness_din_st_from_loudness(N, N_specific, weighting=weighting)

    return S