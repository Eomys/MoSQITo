# -*- coding: utf-8 -*-


# Local imports
from mosqito.sq_metrics import loudness_zwst_freq
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import sharpness_din_from_loudness

from numpy import arange, interp

def sharpness_din_freq(spectrum, freqs, weighting="din", field_type="free"):
    """Acoustic sharpness calculation according to different methods
      (Aures, Von Bismarck, DIN 45692, Fastl) from a complex spectrum.

    Parameters:
    ----------
    signal: numpy.array
        A RMS spectrum.
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
    # Check the inputs
    if len(spectrum) != len(freqs):
        raise ValueError(
            'Input spectrum and frequency axis must have the same shape')
    
    if (freqs.max() < 24000) or (freqs.min() > 24):
        print("[WARNING] freqs argument is not wide enough to cover the full audio range. Missing frequency bands will be filled with 0. To fulfill the standard requirements, the frequency axis should go from 24Hz up to 24 kHz."
        )
        df = freqs[1] - freqs[0]
        spectrum = interp(arange(0,24000+df, df), freqs, spectrum)
        freqs = arange(0,24000+df, df)

    # Compute loudness
    N, N_specific, _ = loudness_zwst_freq(
        spectrum, freqs, field_type=field_type)

    if len(spectrum.shape) > 1:
        raise ValueError(
            "With a 2D spectrum use 'sharpness_din_perseg' calculation.")

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(N, N_specific, weighting=weighting)

    return S
