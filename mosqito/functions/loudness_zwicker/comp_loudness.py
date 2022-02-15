# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:23:56 2020

@author: martin_g for eomys
"""

# Standard import
import numpy as np

# Local imports
from mosqito.functions.noct_spectrum.comp_noct_spectrum import comp_noct_spectrum
from mosqito.functions.loudness_zwicker.loudness_zwicker_stationary import (
    loudness_zwicker_stationary,
)
from mosqito.functions.loudness_zwicker.loudness_zwicker_time import (
    loudness_zwicker_time,
)
from mosqito.functions.loudness_zwicker.calc_third_octave_levels import (
    calc_third_octave_levels,
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
    output : dict
        {
            "name": "Loudness",
            "values": N: float/numpy.array
                loudness value
            "specific values": N_specific: numpy.array
                specific loudness values
            "freqs": bark_axis: numpy.array
                frequency axis corresponding to N_specific values in bark
        }
    """

    if is_stationary == True:
        third_spec, freq = comp_noct_spectrum(signal, fs, fmin=24, fmax=12600)
        third_spec = 20 * np.log10(third_spec / 2e-5)
        N, N_specific = loudness_zwicker_stationary(third_spec, freq, field_type)
    elif is_stationary == False:
        spec_third, _, _ = calc_third_octave_levels(signal, fs)
        N, N_specific = loudness_zwicker_time(spec_third, field_type)

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
    output : dict
        {
            "name": "Loudness",
            "values": N: float/numpy.array
                loudness value
            "specific values": N_specific: numpy.array
                specific loudness values
            "freqs": bark_axis: numpy.array
                frequency axis corresponding to N_specific values in bark
        }
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
