# -*- coding: utf-8 -*-

# Standard imports
from numpy import arange, empty

# Local imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.comp_spectrum import comp_spectrum
from mosqito.sq_metrics.roughness.roughness_dw._roughness_dw_main_calc import (
    _roughness_dw_main_calc,
)
from mosqito.sq_metrics.roughness.roughness_dw._gzi_weighting import _gzi_weighting
from mosqito.sq_metrics.roughness.roughness_dw._H_weighting import _H_weighting


def roughness_dw(signal, fs, overlap=0.5):
    """
    Computes the roughness according to Daniel and Weber method
    from a time signal

    This function computes the global and specific roughness values
    of a signal sampled at 48 kHz.

    Parameters
    ----------
    signal : array_like or DataTime object
        Input time signal in Pa
    fs : float
        Sampling frequency [Hz]
    overlap : float
        Overlapping coefficient for the time windows of 200ms

    Returns
    -------
    R : numpy.array
        Roughness value in [asper]
    R_spec : numpy.array
        Specific roughness over bark axis
    bark_axis : numpy.array
        Frequency axis in [bark]
    time : numpy.array
        Time axis in [s]

    See Also
    --------
    .roughness_dw_freq : Roughness computation from a sound spectrum

    Notes
    -----
    The model consists of a parallel processing structure made up
    of successive stages to calculate intermediate specific roughnesses :math:`R'`,
    which are summed up to determine the total roughness :math:`R`:

    .. math::
        R=0.25\\sum_{i=1}^{47}R'_{i}

    References
    ----------
    :cite:empty:`R-roughnessDW`

    .. bibliography::
        :keyprefix: R-

    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import roughness_dw
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> fc=1000
       >>> fmod=70
       >>> fs=44100
       >>> d=0.2
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> stimulus = (0.5 * (1 + np.sin(2 * np.pi * fmod * time))* np.sin(2 * np.pi * fc * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> R, R_specific, bark, time = roughness_dw(stimulus, fs=44100, overlap=0)
       >>> plt.plot(bark, R_specific)
       >>> plt.xlabel("Bark axis [Bark]")
       >>> plt.ylabel("Specific roughness [Asper/Bark]")
       >>> plt.title("Roughness = " + f"{R[0]:.2f}" + " [Asper]")
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

    spec, _ = comp_spectrum(sig, fs, nfft="default", window="blackman", db=False)

    # Frequency axis in Hertz
    freq_axis = arange(1, nperseg // 2 + 1, 1) * (fs / nperseg)

    # Initialization of the weighting functions H and g
    hWeight = _H_weighting(nperseg, fs)
    # Aures modulation depth weighting function
    gzi = _gzi_weighting(arange(1, 48, 1) / 2)

    if len(spec.shape) > 1:
        R = empty((nseg))
        R_spec = empty((47, nseg))
        for i in range(nseg):
            R[i], R_spec[:, i], bark_axis = _roughness_dw_main_calc(
                spec[:, i], freq_axis, fs, gzi, hWeight
            )
    else:
        R, R_spec, bark_axis = _roughness_dw_main_calc(
            spec, freq_axis, fs, gzi, hWeight
        )

    return R, R_spec, bark_axis, time
