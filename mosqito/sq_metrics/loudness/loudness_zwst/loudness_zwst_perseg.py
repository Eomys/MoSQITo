# -*- coding: utf-8 -*-

# Local application imports
from mosqito.utils import time_segmentation
from mosqito.sq_metrics.loudness.loudness_zwst.loudness_zwst import loudness_zwst


def loudness_zwst_perseg(signal, fs, nperseg=4096, noverlap=None, field_type="free"):
    """
    Compute the loudness value per segments from a time signal

    This function computes the acoustic loudness according to Zwicker method (ISO.532-1:2017)
    by segmentation of a stationary signal.

    Parameters
    ------------
    signal: array_like
        Input time signal in [Pa].
    fs : float, optional
        Sampling frequency, can be omitted if the input is a DataTimeobject.
        Default to None
    nperseg: int, optional
        Length of each segment. Defaults to 4096.
    noverlap: int, optional
        Number of points to overlap between segments.
        If None, noverlap = nperseg / 2. Defaults to None.
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'

    Returns
    --------
    N : float
        Overall loudness [sones], size (Ntime,).
    N_specific : numpy.ndarray
        Specific loudness [sones/bark], size (Nbark, Ntime).
    bark_axis : numpy.ndarray
        Bark axis, size (Nbark,).
    time_axis : numpy.ndarray
        Time axis, size (Ntime,).

    Warning
    -------
    N : numpy.array
        The overall loudness array [sones], size (Ntime,).
    N_specific : numpy.ndarray
        The specific loudness array [sones/bark], size (Nbark, Ntime).
    bark_axis: numpy.array
        The Bark axis array, size (Nbark,).
    time_axis: numpy.array
        The time axis array, size (Ntime,).
	The sampling frequency of the signal must be >= 48 kHz to fulfill requirements.
    If the provided signal doesn't meet the requirements, it will be resampled.


    See Also
    ---------
    .loudness_zwst : Loudness computation for a stationary time signal
    .loudness_zwst_freq : Loudness computation from a sound spectrum
    .loudness_zwtv : Loudness computation for a non-stationary time signal

    Notes
    ------
    For each considered segment, the total loudness :math:`N` is computed as the integral of the specific loudness :math:`N'` measured in sone/bark, over the Bark scale.
    The values of specific loudness are evaluated from third octave band levels as function of critical band rate :math:`z` in Bark.

    .. math::
        N=\\int_{0}^{24Bark}N'(z)\\textup{dz}

    Due to normative continuity, the method is in accordance with ISO 226:1987 equal loudness contours
    instead of ISO 226:2003, as defined in the following standards:
        * ISO 532:1975 (method B)
        * DIN 45631:1991
        * ISO 532-1:2017 (method 1)

    References
    -----------
    :cite:empty:`L_zw-ZF91`
    :cite:empty:`L_zw-ISO.532-1:2017`
    
    .. bibliography::
        :keyprefix: L_zw-

    Examples
    ---------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import loudness_zwst_perseg
       >>> import matplotlib.pyplot as plt
       >>> import numpy as np
       >>> fs=48000
       >>> d=1
       >>> dB=60
       >>> time = np.arange(0, d, 1/fs)
       >>> f = np.linspace(1000,5000, len(time))
       >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
       >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
       >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
       >>> stimulus = stimulus * ampl
       >>> N, N_spec, bark_axis, time_axis = loudness_zwst_perseg(stimulus, fs=fs)
       >>> plt.plot(time_axis, N)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Loudness [Sone]")
    """
    if fs < 48000:
        print(
            "[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
        )
        from scipy.signal import resample

        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000

    # Time signal segmentation
    signal, time_axis = time_segmentation(signal, fs, nperseg, noverlap)

    # Compute loudness
    N, N_specific, bark_axis = loudness_zwst(signal, fs, field_type=field_type)

    return N, N_specific, bark_axis, time_axis
