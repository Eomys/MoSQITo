# -*- coding: utf-8 -*-

from numpy import clip, sqrt, mean, array, linspace, sum, log10

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
    N : float
        Overall loudness representative value [sone_HMS].
    N_time : numpy.ndarray
        Loudness over time [sone_HMS], size (Ntime,).
    N_specific : numpy.ndarray
        Specific loudness [sone_HMS/bark], size (Nbark, Ntime).
	Each of the 53 elements of the list corresponds to the time-dependant specific loudness for a given bark band. Can be a ragged array if a different sb/sh are used for each band.
    bark_axis : numpy.ndarray
        Corresponding bark axis, size (Nbark,).
    time_axis : numpy.ndarray
        Time axis, size (Ntime,).
    bark_axis: array_like
        Bark axis array, size (Nbark,).

    Warning
    -------
    The sampling frequency of the signal must be 48 kHz.

    See Also
    --------
    .loudness_zwst : Zwicker and Fastl loudness computation for a stationary time signal
    .loudness_zwtv : Zwicker and Fastl loudness computation for a non-stationary time signal

    References
    ----------
    :cite:empty:`L_ecma-ECMA-418-2`

    .. bibliography::
        :keyprefix: L_ecma-

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
    block_array, time_array = _ecma_time_segmentation(bandpass_signals, sb, sh, n_new)

    # Rectification (5.1.6)
    block_array_rect = clip(block_array, a_min=0.00, a_max=None)

    # Calculation of specific loudness (5.1.7 to 5.1.9)
    N_spec = []
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
        N_spec.append(N_prime)

    # Time dependent values (eq. 116)
    delta_z = 0.5
    N_time = sum(N_spec, axis=0) * delta_z

    # Single-value loudness (eq. 117)
    e = 1 / log10(2)
    N = (mean(N_time**e)) ** (1 / e)

    bark_axis = linspace(0.5, 26.5, num=53, endpoint=True)

    return N, N_time, N_spec, bark_axis, time_array
