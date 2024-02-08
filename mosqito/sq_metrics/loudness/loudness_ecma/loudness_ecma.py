# -*- coding: utf-8 -*-

from numpy import clip, sqrt, mean, array, linspace

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import (
    _band_pass_signals,
)

from mosqito.sq_metrics.loudness.loudness_ecma._ecma_time_segmentation import (
    _ecma_time_segmentation,
)

from mosqito.sq_metrics.loudness.loudness_ecma._nonlinearity import _nonlinearity

from mosqito.sq_metrics.loudness.loudness_ecma._preprocessing import (
    _preprocessing,
)

# Data import
# Threshold in quiet
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z



def loudness_ecma(signal, fs, sb=2048, sh=1024):
    """Calculation of the specific and total loudness according to ECMA-418-2
    (2nd Ed, 2022), Section 5.

    Parameters
    ----------
    signal: numpy.array
        time signal values in 'Pa'. The sampling frequency of the signal must be 48000 Hz.
    sb: int or list of int
        block size.
    sh: int or list of int
        Hop size.

    Returns
    -------
    n_specific: list of numpy.array
        Specific Loudness [sone_HMS per Bark]. Each of the 53 element of the list corresponds to the time-dependant
        specific loudness for a given bark band. Can be a ragged array if a different sb/sh are used for each band.

    bark_axis: numpy.array
        Bark axis

    """
    if fs != 48000:
        print(
            "[Warning] Signal resampled to 48 kHz fulfill the standard requirements and allow calculation."
        )
        from scipy.signal import resample

        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
    
    
    # Windowing and zero-padding (5.1.2)
    signal, n_new = _preprocessing(signal, sb, sh)
    
    # Computaton of band-pass signals (5.1.3 to 5.1.4)
    bandpass_signals = _band_pass_signals(signal)

    # Segmentation into blocks (5.1.5)
    block_array, _ = _ecma_time_segmentation(bandpass_signals, sb, sh, n_new)
    
    # Rectification (5.1.6)
    block_array_rect = clip(block_array, a_min=0.00, a_max=None)


    # Calculation of specific loudness (5.1.7 to 5.1.9)
    n_specific = []
    for band_number in range(53):
        # root mean square values (eq. 22)
        rms_block_value = sqrt(
            2 * mean(array(block_array_rect[band_number]) ** 2, axis=1)
        )
        # non-linear transformation of sound pressure to specific loudness
        a_prime = _nonlinearity(rms_block_value)
        # specific loudness considering the lower threshold of hearing.
        a_prime[a_prime < ltq_z[band_number]] = ltq_z[band_number]
        N_prime = a_prime - ltq_z[band_number]
        n_specific.append(N_prime)

    bark_axis = linspace(0.5, 26.5, num=53, endpoint=True)
    
    return n_specific, bark_axis
