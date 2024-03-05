# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np

# Local applications imports
from mosqito.sq_metrics.loudness.loudness_zwst._main_loudness import _main_loudness
from mosqito.sq_metrics.loudness.loudness_zwst._calc_slopes import _calc_slopes
from mosqito.sq_metrics.loudness.loudness_zwtv._nonlinear_decay import _nl_loudness
from mosqito.sq_metrics.loudness.loudness_zwtv._temporal_weighting import (
    _temporal_weighting,
)
from mosqito.sq_metrics.loudness.loudness_zwtv._third_octave_levels import (
    _third_octave_levels,
)


def loudness_zwtv(signal, fs, field_type="free"):
    """Calculate Zwicker-loudness for time-varying signals
    Calculate the acoustic loudness according to Zwicker method for
    time-varying signals.
    Normatice reference:
        DIN 45631/A1:2010
        ISO 532-1:2017 (method 2)
    The code is based on C program source code published alongside
    with ISO 532-1 standard.
    Note that for reasons of normative continuity, as defined in the
    preceeding standards, the method is in accordance with
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003)
    Parameters
    ----------
    signal : numpy.array
        A time signal values [Pa].
    fs : integer
        Sampling frequency.
    field_type : str
        Type of soundfield corresponding to signal ("free" by or "diffuse").

    Outputs
    -------
    N : float
        Calculated loudness [sones], size (Ntime,).
    N_specific : numpy.ndarray
        Specific loudness [sones/bark], size (Nbark, Ntime).
    bark_axis : numpy.ndarray
        Corresponding bark axis, size (Nbark,).
    time_axis : numpy.ndarray
        Time axis, size (Ntime,).

    """

    if fs < 48000:
        print(
            "[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
        )
        from scipy.signal import resample

        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000

    # Compute third octave band spectrum vs. time
    spec_third, time_axis, _ = _third_octave_levels(signal, fs)

    # Calculate core loudness (vectorized version)
    core_loudness = _main_loudness(spec_third, field_type)

    #
    # Nonlinearity
    core_loudness = _nl_loudness(core_loudness)
    #
    # Calculation of specific loudness
    loudness, spec_loudness = _calc_slopes(core_loudness)

    # temporal weigthing
    filt_loudness = _temporal_weighting(loudness)
    #
    # Decimation from temporal resolution 0.5 ms to 2ms and return
    dec_factor = 4
    N = filt_loudness[::dec_factor]
    N_spec = spec_loudness[:, ::dec_factor]
    time_axis = time_axis[::dec_factor]
    #
    # Build bark axis
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))

    return N, N_spec, bark_axis, time_axis
