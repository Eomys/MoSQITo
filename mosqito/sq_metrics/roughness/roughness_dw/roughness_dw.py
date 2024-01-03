# -*- coding: utf-8 -*-

# Standard imports
import numpy as np

# Local imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.spectrum import spectrum
from mosqito.sq_metrics.roughness.roughness_dw._roughness_dw_main_calc import (
    _roughness_dw_main_calc,
)
from mosqito.sq_metrics.roughness.roughness_dw._gzi_weighting import _gzi_weighting
from mosqito.sq_metrics.roughness.roughness_dw._H_weighting import _H_weighting


def roughness_dw(signal, fs, overlap=0.5):
    """Roughness calculation of a signal sampled at 48kHz.

    The code is based on the algorithm described in "Psychoacoustical roughness:
    implementation of an optimized model" by Daniel and Weber in 1997.
    The roughness model consists of a parallel processing structure that is made up
    of successive stages and calculates intermediate specific roughnesses R_spec,
    which are summed up to determine the total roughness R.

    Parameters
    ----------
    signal :numpy.array
        A time signal [Pa]
    fs : float
        Sampling frequency [Hz]
    overlap : float
        Overlapping coefficient for the time windows of 200ms

    Outputs
    -------
    R : numpy.array
        Roughness [asper].
    R_spec : numpy.array
        Specific roughness over bark axis.
    bark_axis : numpy.array
        Frequency axis [bark].
    time : numpy.array
        Time axis [s].

    """

    # Number of points within each frame according to the time resolution of 200ms
    nperseg = int(0.2 * fs)
    # Overlapping segment length
    noverlap = int(overlap * nperseg)
    # reshaping of the signal according to the overlap and time proportions
    sig, time = time_segmentation(
        signal, fs, nperseg=nperseg, noverlap=noverlap, is_ecma=False
    )
    if len(sig.shape) == 1:
        nseg = 1
    else:
        nseg = sig.shape[1]

    spec, _ = spectrum(sig, fs, nfft="default", window="blackman", db=False)

    # Frequency axis in Hertz
    freq_axis = np.arange(1, nperseg // 2 + 1, 1) * (fs / nperseg)

    # Initialization of the weighting functions H and g
    hWeight = _H_weighting(nperseg, fs)
    # Aures modulation depth weighting function
    gzi = _gzi_weighting(np.arange(1, 48, 1) / 2)

    R = np.zeros((nseg))
    R_spec = np.zeros((47, nseg))
    if len(spec.shape) > 1:
        for i in range(nseg):
            R[i], R_spec[:, i], bark_axis = _roughness_dw_main_calc(
                spec[:, i], freq_axis, fs, gzi, hWeight
            )
    else:
        R, R_spec, bark_axis = _roughness_dw_main_calc(
            spec, freq_axis, fs, gzi, hWeight
        )

    return R, R_spec, bark_axis, time
