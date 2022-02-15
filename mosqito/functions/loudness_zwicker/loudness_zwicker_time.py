# -*- coding: utf-8 -*-
"""
@date Created on Thu Mar 26 2020
@author martin_g for Eomys
"""

# Standard library imports
import numpy as np

# Local applications imports
from mosqito.functions.loudness_zwicker.loudness_zwicker_shared import (
    calc_main_loudness as calc_main_loudness,
)
from mosqito.functions.loudness_zwicker.loudness_zwicker_nonlinear_decay import (
    calc_nl_loudness,
)
from mosqito.functions.loudness_zwicker.loudness_zwicker_shared import calc_slopes
from mosqito.functions.loudness_zwicker.loudness_zwicker_temporal_weighting import (
    loudness_zwicker_temporal_weighting,
)


def loudness_zwicker_time(third_octave_levels, field_type):
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
    third_octave_levels : numpy.ndarray
        rms acoustic pressure [Pa] per third octave versus time
        (temporal resolution = 0.5ms)
    field_type : str
        Type of soundfield corresponding to signal ("free" by
        default or "diffuse")

    Outputs
    -------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    bark_axis : numpy.ndarray
        Corresponding bark axis
    """

    # Calculate core loudness (vectorized version)
    core_loudness = calc_main_loudness(third_octave_levels, field_type)

    #
    # Nonlinearity
    core_loudness = calc_nl_loudness(core_loudness)
    #
    # Calculation of specific loudness
    loudness, spec_loudness  = calc_slopes(core_loudness)

    # temporal weigthing
    filt_loudness = loudness_zwicker_temporal_weighting(loudness)
    #
    # Decimation from temporal resolution 0.5 ms to 2ms and return
    dec_factor = 4
    N = filt_loudness[::dec_factor]
    N_spec = spec_loudness[:, ::dec_factor]
    return N, N_spec
