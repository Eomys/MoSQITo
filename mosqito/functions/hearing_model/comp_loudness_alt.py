# -*- coding: utf-8 -*-
"""
@author: Daniel Jiménez-Caminero Costa
"""
import numpy as np
import matplotlib.pyplot as plt

# Project Imports
from mosqito.functions.hearing_model.rectified_band_pass_signals import (
    rectified_band_pass_signals,
)


def comp_loudness(signal, sb=2048, sh=1024):
    """Calculation of specific loudness and total loudness of an input signal according to ECMA-418-2. It describes the
    loudness excitation in a critical band per Bark. The output of the signal consists in a pair of array lists, one
    for specific loudness and the other one for total loudness.

    Parameters
    ----------
    validation: boolean
        Default value is set to 'False'. It is used to mark whether complete validation is done or not.

    signal: numpy.array
        'Pa', time signal values. It can be, stereo (2 dimensions) or mono (1 dimension).The sampling frequency of the
        signal must be 48000 Hz.

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

    """ CONSIDERATION OF THRESHOLD IN QUIET """
    # "The specific loudness in each band z is zero if it is at or below a critical-band-dependent specific loudness
    # threshold LTQ(z)"
    ltq_z = [
        0.3310,
        0.1625,
        0.1051,
        0.0757,
        0.0576,
        0.0453,
        0.0365,
        0.0298,
        0.0247,
        0.0207,
        0.0176,
        0.0151,
        0.0131,
        0.0115,
        0.0103,
        0.0093,
        0.0086,
        0.0081,
        0.0077,
        0.0074,
        0.0073,
        0.0072,
        0.0071,
        0.0072,
        0.0073,
        0.0074,
        0.0076,
        0.0079,
        0.0082,
        0.0086,
        0.0092,
        0.0100,
        0.0109,
        0.0122,
        0.0138,
        0.0157,
        0.0172,
        0.0180,
        0.0180,
        0.0177,
        0.0176,
        0.0177,
        0.0182,
        0.0190,
        0.0202,
        0.0217,
        0.0237,
        0.0263,
        0.0296,
        0.0339,
        0.0398,
        0.0485,
        0.0622,
    ]

    """ NON-LINEARITY. SOUND PRESSURE INTO SPECIFIC LOUDNESS """
    p_0 = 2e-5
    # c_N: In sones/bark
    c_N = 0.0217406
    alpha = 1.50
    v_i = np.array(
        [1.0, 0.6602, 0.0864, 0.6384, 0.0328, 0.4068, 0.2082, 0.3994, 0.6434]
    )
    thresh = np.array([15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0])
    p_ti = p_0 * 10 ** (thresh / 20)

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
        exp = (v_i[1:] - v_i[:-1]) / alpha
        prod = np.prod(
            (1 + (rms_block_value / p_ti[:, np.newaxis]) ** alpha)
            ** exp[:, np.newaxis],
            axis=0,
        )
        a_prime = c_N * rms_block_value / p_0 * prod

        """SPECIFIC LOUDNESS CONSIDERING THE THRESHOLD IN QUIET (5.1.8)

        The next calculation helps us obtain the result for the specific loudness - specific loudness with
        consideration of the lower threshold of hearing. 
        """

        a_prime[a_prime < ltq_z[band_number]] = ltq_z[band_number]
        N_prime = a_prime - ltq_z[band_number]
        n_array.append(N_prime)

    return n_array
