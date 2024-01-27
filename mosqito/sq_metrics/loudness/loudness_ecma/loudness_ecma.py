# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa

[Jan 2024] Updated to ECMA-418-2, 2nd Ed (2022)
"""
import numpy as np

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import (
    _band_pass_signals,
)

from mosqito.sq_metrics.loudness.loudness_ecma._ecma_time_segmentation import (
    _ecma_time_segmentation,
)

from mosqito.sq_metrics.loudness.loudness_ecma._nonlinearity import _nonlinearity

from mosqito.sq_metrics.loudness.loudness_ecma._windowing_zeropadding import (
    _windowing_zeropadding,
)

# Data import
# Threshold in quiet
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z



def loudness_ecma(signal, sb=2048, sh=1024):
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
    
    # 5.1.2 Windowing and zero-padding
    signal, n_new = _windowing_zeropadding(signal, sb, sh)
    
    
    # 5.1.3 to 5.1.4 - Computaton of band-pass signals
    bandpass_signals = _band_pass_signals(signal)

    # 5.1.5 Segmentation into blocks
    block_array, time_array = _ecma_time_segmentation(bandpass_signals, sb, sh,
                                                      n_new)
    
    # 5.1.6 Rectification (Eq. 21)
    block_array_rect = np.clip(block_array, a_min=0.00, a_max=None)

    # ************************************************************************
    # Copied from old version
    
    # # sb and sh for Tonality
    # z = np.linspace(0.5, 26.5, num=53, endpoint=True)
    # sb = np.ones(53, dtype="int")
    # sh = np.ones(53, dtype="int")
    # sb[z <= 1.5] = 8192
    # sh[z <= 1.5] = 2048
    # sb[np.all([z >= 2, z <= 8], axis=0)] = 4096
    # sh[np.all([z >= 2, z <= 8], axis=0)] = 1024
    # sb[np.all([z >= 8.5, z <= 12.5], axis=0)] = 2048
    # sh[np.all([z >= 8.5, z <= 12.5], axis=0)] = 512
    # sb[z >= 13] = 1024
    # sh[z >= 13] = 256

    # ************************************************************************
    # Sections 5.1.7 to 5.1.9 
    
    n_specific = []
    for band_number in range(53):
        # ROOT-MEAN-SQUARE (section 5.1.7)
        # After the segmentation of the signal into blocks, root-mean square values of each block are calculated
        # according to Formula 22.
        rms_block_value = np.sqrt(
            2 * np.mean(np.array(block_array_rect[band_number]) ** 2, axis=1)
        )

        # NON-LINEARITY (section 5.1.8)
        # This section covers the other part of the calculations needed to consider the non-linear transformation
        # of sound pressure to specific loudness that does the the auditory system. After this point, the
        # computation is done equally to every block in which we have divided our signal.
        a_prime = _nonlinearity(rms_block_value)

        # SPECIFIC LOUDNESS CONSIDERING THE THRESHOLD IN QUIET (section 5.1.9)
        # The next calculation helps us obtain the result for the specific loudness - specific loudness with
        # consideration of the lower threshold of hearing.
        a_prime[a_prime < ltq_z[band_number]] = ltq_z[band_number]
        N_prime = a_prime - ltq_z[band_number]
        n_specific.append(N_prime)

    bark_axis = np.linspace(0.5, 26.5, num=53, endpoint=True)
    
    return n_specific, bark_axis
