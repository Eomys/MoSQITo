# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import matplotlib.pyplot as plt

# Project Imports
from mosqito.functions.loudness_ecma.rectified_band_pass_signals import (
    rectified_band_pass_signals,
)
from mosqito.functions.loudness_ecma.loudness_function import (
    loudness_function as loudness_function,
)

# Data import
# Threshold in quiet
from mosqito.functions.loudness_ecma.loudness_ecma_data import ltq_z


def comp_loudness(signal, sb=2048, sh=1024):
    """Calculation of specific loudness and total loudness of an input signal according to ECMA-418-2. It describes the
    loudness excitation in a critical band per Bark. The output of the signal consists in a pair of array lists, one
    for specific loudness and the other one for total loudness.

    Parameters
    ----------
    signal: numpy.array
        time signal valuesin 'Pa'. It can be, stereo (2 dimensions) or mono (1 dimension).The sampling frequency of the
        signal must be 48000 Hz.
    sb: int or list of int
        block size.
    sh: int or list of int
        Hop size.

    Returns
    -------
    n_array: numpy.array
        'Sone per Bark'. It is a numpy array that is arranged as a matrix. Each matrix row represents a certain block of
        audio (in chronological order) and each matrix column stores the value of the specific loudness for that block
        and that specific band (column number). If the input signal is stereo, another matrix dimension is added.

    t_array: numpy.array
        'Sone per Bark'. As well as "n_array", it is a numpy array that is arranged as a matrix. Each matrix row
        represents a certain block of audio (in chronological order). If the input signal is stereo, another matrix
        dimension is added.
    """

    """Rectified band-pass signals (5.1.5)"""
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

    block_array_rect = rectified_band_pass_signals(signal, sb, sh)

    n_array = []
    for band_number in range(53):
        """ROOT-MEAN-SQUARE (5.1.6)

        After the segmentation of the signal into blocks, root-mean square values of each block are calculated in
        Formula 17).
        """

        rms_block_value = np.sqrt(
            2 * np.mean(np.array(block_array_rect[band_number]) ** 2, axis=1)
        )

        """NON-LINEARITY (5.1.7)

        This section covers the other part of the calculations needed to consider the non-linear transformation
        of sound pressure to specific loudness that does the the auditory system. After this point, the
        computation is done equally to every block in which we have divided our signal.
        """
        a_prime = loudness_function(rms_block_value)

        """SPECIFIC LOUDNESS CONSIDERING THE THRESHOLD IN QUIET (5.1.8)

        The next calculation helps us obtain the result for the specific loudness - specific loudness with
        consideration of the lower threshold of hearing. 
        """

        a_prime[a_prime < ltq_z[band_number]] = ltq_z[band_number]
        N_prime = a_prime - ltq_z[band_number]
        n_array.append(N_prime)

    return n_array
