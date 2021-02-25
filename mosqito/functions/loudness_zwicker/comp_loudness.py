# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:23:56 2020

@author: martin_g for eomys
"""

# Standard import
import numpy as np

# Local imports
from mosqito.functions.oct3filter.comp_third_spectrum import comp_third_spec
from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import (
    loudness_zwicker_stationary,
)
from mosqito.functions.loudness_zwicker.loudness_zwicker_time import (
    loudness_zwicker_time,
)


def comp_loudness(is_stationary, signal, fs, field_type="free"):
    """Acoustic loudness calculation according to Zwicker method for
    stationary and time-varying signals.

    Parameters
    ----------
    is_stationary: boolean
        TRUE if the signal is stationary, FALSE if it is time-varying
    signal : numpy.array
        time signal values
    fs : integer
        sampling frequency
    field-type: string
        'free' by default or 'diffuse'

    Outputs
    -------
    N: float/numpy.array
        loudness value
    N_specific: numpy.array
        specific loudness values
    bark_axis: numpy.array
        frequency axis correpsondong to N_specific values in bark
    """

    third_spec = comp_third_spec(is_stationary, signal, fs)

    if is_stationary == True:
        N, N_specific = loudness_zwicker_stationary(
            third_spec["values"], third_spec["freqs"], field_type
        )
    elif is_stationary == False:
        N, N_specific = loudness_zwicker_time(third_spec["values"], field_type)

    # critical band rate scale
    bark_axis = np.linspace(0.1, 24, int(24 / 0.1))

    output = {
        "name": "Loudness",
        "values": N,
        "specific values": N_specific,
        "freqs": bark_axis,
    }

    return output


def comp_loudness_from_3spec(
    is_stationary, third_spec, third_axis=[], field_type="free"
):
    """Acoustic loudness calculation according to Zwicker method for
    stationary and time-varying signals.

    Parameters
    ----------
    is_stationary: boolean
        TRUE if the signal is stationary, FALSE if it is time-varying
    third_spec: numpy.array
        third octave spectrum
    third_axis: numpy.array
        third-octav frequency axis
    field-type: string
        'free' by default or 'diffuse'

    Outputs
    -------
    N: float/numpy.array
        loudness value
    N_specific: numpy.array
        specific loudness values
    bark_axis: numpy.array
        frequency axis correpsondong to N_specific values in bark
    """

    if is_stationary == True:
        N, N_specific = loudness_zwicker_stationary(third_spec, third_axis, field_type)
    elif is_stationary == False:
        N, N_specific = loudness_zwicker_time(third_spec, field_type)

    if third_axis == []:
        # critical band rate scale
        third_axis = np.linspace(0.1, 24, int(24 / 0.1))

    output = {
        "name": "Loudness",
        "values": N,
        "specific values": N_specific,
        "freqs": third_axis,
    }

    return output
