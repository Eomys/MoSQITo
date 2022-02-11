# -*- coding: utf-8 -*-
"""
@date Created on Tue Feb 25 2020
@author martin_g for Eomys
"""

# Third party imports
import numpy as np

# Local application imports
from mosqito.functions.loudness_zwicker.loudness_zwicker_shared import (
    calc_main_loudness,
)
from mosqito.functions.loudness_zwicker.loudness_zwicker_shared import calc_slopes


def loudness_zwicker_stationary(spec_third, third_axis=[], field_type="free"):
    """Zwicker-loudness calculation for stationary signals

    Calculates the acoustic loudness according to Zwicker method for
    stationary signals.
    Normatice reference:
        ISO 532:1975 (method B)
        DIN 45631:1991
        ISO 532-1:2017 (method 1)
    The code is based on BASIC program published in "Program for
    calculating loudness according to DIN 45631 (ISO 532B)", E.Zwicker
    and H.Fastl, J.A.S.J (E) 12, 1 (1991).
    Note that due to normative continuity, as defined in the
    preceeding standards, the method is in accordance with
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003)

    Parameters
    ----------
    spec_third : numpy.ndarray
        A third octave band spectrum [dB ref. 2e-5 Pa]
    third_axis : numpy.ndarray
        Normalized center frequency of third octave bands [Hz]
    field_type : str
        Type of soundfield corresponding to spec_third ("free" by
        default or "diffuse")

    Outputs
    -------
    N : float
        Calculated loudness [sones]
    N_specific : numpy.ndarray
        Specific loudness [sones/bark]
    """
    #
    # Input parameters control and formating
    fr = [
        25,
        31.5,
        40,
        50,
        63,
        80,
        100,
        125,
        160,
        200,
        250,
        315,
        400,
        500,
        630,
        800,
        1000,
        1250,
        1600,
        2000,
        2500,
        3150,
        4000,
        5000,
        6300,
        8000,
        10000,
        12500,
    ]
    if field_type != "diffuse" and field_type != "free":
        raise ValueError("ERROR: field_type should be either 'diffuse' or 'free'")
    if len(spec_third) != 28:
        raise ValueError("ERROR: spectrum must contains 28 third octave bands values")
    if len(third_axis) == 0:
        third_axis = fr
    elif (len(third_axis) == 28 and np.all(third_axis != fr)) or len(third_axis) < 28:
        raise ValueError(
            """ERROR: third_axis does not contains 1/3 oct between 25 and 
            12.5 kHz. Check the input parameters"""
        )
    else:
        # TODO: manage spectrum and third_axis longer than 28 (extract data
        # between 25 and 12.5 kHz)
        pass
    #    if (min(spec_third) < -60 or max(spec_third) > 120):
    # TODO: replace value below -60 by -60 and raise a warning
    #        raise ValueError(
    #            """ERROR: Third octave levels must be within interval
    #            [-60, 120] dB ref. 2e-5 Pa (for model validity) """
    #        )
    #
    #
    # Calculate main loudness
    Nm = calc_main_loudness(spec_third, field_type)
    #
    # Calculation of specific loudness pattern and integration of overall
    # loudness by attaching slopes towards higher frequencies
    N, N_specific = calc_slopes(Nm)

    return N, N_specific
