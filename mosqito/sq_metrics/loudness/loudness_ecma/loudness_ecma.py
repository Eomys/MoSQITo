# -*- coding: utf-8 -*-

from numpy import mean, array, sqrt, linspace, sum

# Project Imports
from mosqito.sq_metrics.loudness.loudness_ecma._rectified_band_pass_signals import (
    _rectified_band_pass_signals,
)
from mosqito.sq_metrics.loudness.loudness_ecma._nonlinearity import _nonlinearity
from mosqito.sq_metrics.loudness.loudness_ecma._loudness_ecma_data import ltq_z


def loudness_ecma(signal, sb=2048, sh=1024):
    """
    Returns the loudness value 
    
    This function computes the acoustic loudness according to ECMA-418-2 section 5 method for
    stationary signals.
    
    Parameters
    ----------
    signal: numpy.array
        Signal time values [Pa]. The sampling frequency of the signal must be 48000 Hz.
    sb: int or list of int
        Block size.
    sh: int or list of int
        Hop size.

    Returns
    -------
    N_specific : list of numpy.array
        Specific Loudness [sone_HMS per Bark]. Each of the 53 elements of the list corresponds to the time-dependant
        specific loudness for a given bark band. Can be a ragged array if a different sb/sh are used for each band.
    bark_axis: array_like
        Bark axis array, size (Nbark,).
        
    See Also
    --------
    loudness_zwst : Zwicker and Fastl loudness computation for a stationary time signal
    loudness_zwtv : Zwicker and Fastl loudness computation for a non-stationary time signal

    Notes
    -----
    Normative reference:
        ISO 532:1975 (method B)
        DIN 45631:1991
        ISO 532-1:2017 (method 1)
    Due to normative continuity, as defined in the preceeding standards, the method is in accordance with
    ISO 226:1987 equal loudness contours (instead of ISO 226:2003).
    
    References
    ----------
    .. [ZF] E.Zwicker and H.Fastl, "Program for calculating loudness according to DIN 45631 (ISO 532B)", 
            J.A.S.J (E) 12, 1 (1991).
            
    Warning
    -------
    The sampling frequency of the signal must be 48000 Hz.
            
    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import loudness_ecma
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> f=1000
       >>> fs=48000
       >>> d=0.2
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> N, N_spec, bark_axis, time_axis = loudness_ecma(stimulus)
       >>> plt.plot(time_axis, N)
       >>> plt.xlabel("Frequency band [Bark]")
       >>> plt.ylabel("Loudness [Sone]")
    """

    # Computaton of rectified band-pass signals
    # (section 5.1.2 to 5.1.5 of the standard)
    block_array_rect = _rectified_band_pass_signals(signal, sb, sh)

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

    N_spec = []
    for band_number in range(53):
        # ROOT-MEAN-SQUARE (section 5.1.6)
        # After the segmentation of the signal into blocks, root-mean square values of each block are calculated
        # according to Formula 17.
        rms_block_value = sqrt(
            2 * mean(array(block_array_rect[band_number]) ** 2, axis=1)
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
        N_spec.append(N_prime)

    bark_axis = linspace(0.5, 26.5, num=53, endpoint=True)
    time_axis = linspace(0, len(signal)/48000, len(N_spec[0]))
    N = sum(array(N_spec)*0.5, axis=0)
    
    return N, array(N_spec), bark_axis, time_axis
