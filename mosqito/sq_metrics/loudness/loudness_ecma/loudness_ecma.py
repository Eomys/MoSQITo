# -*- coding: utf-8 -*-
import numpy as np

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._band_pass_signals import _rectified_band_pass_signals
from mosqito.sq_metrics.loudness.loudness_ecma._nonlinearity import _nonlinearity

# Data import
# Threshold in quiet
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z


def loudness_ecma(signal, sb=2048, sh=1024):
    """Calculation of the specific and total loudness according to ECMA-418-2 section 5

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

    # TODO: return time axis (list or list of list)

    # Computaton of rectified band-pass signals
    # (section 5.1.2 to 5.1.5 of the standard)
    block_array_rect = _rectified_band_pass_signals(signal, sb, sh)
    
    n_specific = []
    for band_number in range(53):
        # ROOT-MEAN-SQUARE (section 5.1.6)
        # After the segmentation of the signal into blocks, root-mean square values of each block are calculated
        # according to Formula 17.
        rms_block_value = np.sqrt(
            2 * np.mean(np.array(block_array_rect[band_number]) ** 2, axis=1)
        )

        # NON-LINEARITY (section 5.1.7)
        # This section covers the other part of the calculations needed to consider the non-linear transformation
        # of sound pressure to specific loudness that does the the auditory system. After this point, the
        # computation is done equally to every block in which we have divided our signal.
        a_prime = _nonlinearity(rms_block_value)

        # SPECIFIC LOUDNESS CONSIDERING THE THRESHOLD IN QUIET (section 5.1.8)
        # The next calculation helps us obtain the result for the specific loudness - specific loudness with
        # consideration of the lower threshold of hearing.
        a_prime[a_prime < ltq_z[band_number]] = ltq_z[band_number]
        N_prime = a_prime - ltq_z[band_number]
        n_specific.append(N_prime)

    bark_axis = np.linspace(0.5, 26.5, num=53, endpoint=True)
    return n_specific, bark_axis
