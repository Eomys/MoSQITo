# -*- coding: utf-8 -*-
"""
@date Created on Fri May 22 2020
@author martin_g for Eomys
"""

# Local application import
from mosqito.functions.loudness_zwicker.loudness_zwicker_lowpass_intp import (
    loudness_zwicker_lowpass_intp,
)


def loudness_zwicker_temporal_weighting(loudness):
    """Temporal weighting of total loudness

    Two first-order low-pass filters (time constants 3,5 ms
    and 70 ms) are applied to the sum of the specific loudness
    values in order to simulate the duration dependent behaviour
    of loudness perception for short impulses.

    Parameters
    ----------
    loudness : numpy.ndarray
        Loudness vs. time

    Outputs
    -------
    loudness : numpy.ndarray
        Filtered loudness
    """
    sample_rate = 2000
    tau = 3.5 * 10 ** -3
    filt_loudness_1 = loudness_zwicker_lowpass_intp(loudness, tau, sample_rate)
    tau = 70 * 10 ** -3
    filt_loudness_2 = loudness_zwicker_lowpass_intp(loudness, tau, sample_rate)

    loudness = 0.47 * filt_loudness_1 + 0.53 * filt_loudness_2

    return loudness
