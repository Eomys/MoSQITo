# -*- coding: utf-8 -*-

# Standard library import
from numpy import linspace, log10, empty, nan, logspace, argmin, ravel, abs

# Local functions imports
from mosqito.utils.time_segmentation import time_segmentation
from mosqito.sound_level_meter.comp_spectrum import comp_spectrum
from mosqito.sq_metrics.tonality.tone_to_noise_ecma._tnr_main_calc import _tnr_main_calc


def tnr_ecma_perseg(signal, fs, prominence=False, overlap=0):
    """
    Compute the ECMA-418-1 tone-to-noise ratio per time window.

    Parameters
    ----------
    signal : numpy.ndarray
        One-dimensional sound pressure signal in Pa.
    fs : integer
        Sampling frequency in Hz.
    prominence : bool
        If True, include only prominent tones. If False, also include
        ratios for non-prominent tones. Defaults to False.
    overlap : float
        Controls the step between 500 ms windows. The step in samples is
        ``int(overlap * int(0.5 * fs))``. A zero step (the default) is
        replaced by the window length. For example, ``overlap=0.25``
        gives a 125 ms step at 48 kHz.

    Returns
    -------
    t_tnr : array of float
        Combined TNR in dB for the prominent tones in each window.
    tnr : array of float
        TNR in dB on the frequency-by-time grid.
    promi : array of bool
        Prominence criterion for each detected tone.
    freqs : array_like
        Frequency axis [Hz].
    time : array_like
        Time axis [s].

    See Also
    --------
    .tnr_ecma_freq : TNR computation for a sound spectrum
    .tnr_ecma_st : TNR computation for a stationary signal
    :func:`~mosqito.sq_metrics.tonality.prominence_ratio_ecma.pr_ecma_perseg.pr_ecma_perseg`
        Prominence ratio for a non-stationary signal.

    Notes
    -----
    Each 500 ms window is screened for candidate tones using a
    smoothed-spectrum method based on Bray and Caspary (2008).
    The ratio calculation follows ECMA-418-1. ECMA-418-2 defines a
    separate psychoacoustic tonality metric using the Sottek Hearing Model.

    TNR compares the power of a tone with the masking noise power in its
    critical band. PR compares the power in the tone's critical band
    with the average power in the adjacent critical bands, with a
    bandwidth correction at low frequencies.

    According to ECMA 418-1 standard, TNR can then prove to be more accurate for multiple tones in adjacent critical bands, for example when strong harmonics exist.
    PR can be more effective for multiple tones within the same critical band and is more readily automated to handle such cases.

    The prominence indicator applies the frequency-dependent ECMA-418-1
    criterion to a detected tone's ratio.


    References
    ----------
    :cite:empty:`TNR-ECMA-418-1,TNR-ECMA-418-2,TNR-BrayCaspary2008`

    .. bibliography::
        :keyprefix: TNR-

    Examples
    --------
    The example stimulus is made of white noise + 2 sine waves at 1kHz and 3kHz.

    .. plot::
       :include-source:

        >>> import numpy as np
        >>> import matplotlib.pyplot as plt
        >>> from mosqito.sq_metrics import tnr_ecma_perseg
        >>> fs = 48000
        >>> d = 2
        >>> dB = 60
        >>> time = np.arange(0, d, 1/fs)
        >>> f1 = 1000
        >>> f2 = np.zeros((len(time)))
        >>> f2[len(time)//2:] = 1500
        >>> stimulus = 2 * np.sin(2 * np.pi * f1 * time) + np.sin(2 * np.pi * f2 * time)+ np.random.normal(0,0.5, len(time))
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> t_tnr, tnr, promi, tones_freqs, time = tnr_ecma_perseg(stimulus, fs)
        >>> plt.figure(figsize=(10,8))
        >>> plt.pcolormesh(time, tones_freqs, np.nan_to_num(tnr), vmin=0)
        >>> plt.colorbar(label = "TNR value in dB")
        >>> plt.xlabel("Time [s]")
        >>> plt.ylabel("Frequency [Hz]")
        >>> plt.ylim(90,2000)
    """

    if len(signal.shape) == 1:

        # Number of points within each frame according to the time resolution of 500ms
        nperseg = int(0.5 * fs)
        # Overlappinf segment length
        noverlap = int(overlap * nperseg)
        # Time segmentation of the signal
        sig, time = time_segmentation(
            signal, fs, nperseg=nperseg, noverlap=noverlap, is_ecma=False
        )
        # Number of segments
        nseg = sig.shape[1]
        # Spectrum computation
        spectrum_db, freq_axis = comp_spectrum(sig, fs, db=True)

    else:
        nseg = signal.shape[1]
        time = linspace(0, signal.shape[0] / fs, num=nseg)

        # Compute spectrum
        spectrum_db, freq_axis = comp_spectrum(sig, fs, db=True)

    # compute tnr values
    tones_freqs, tnr_, prom, t_tnr = _tnr_main_calc(spectrum_db, freq_axis)

    # Retore the results in a time vs frequency array
    freqs = logspace(log10(90), log10(11200), num=1000)
    tnr = empty((len(freqs), nseg))
    tnr.fill(nan)
    promi = empty((len(freqs), nseg), dtype=bool)
    promi.fill(False)

    for t in range(nseg):
        for f in range(len(tones_freqs[t])):
            ind = argmin(abs(freqs - tones_freqs[t][f]))
            if prominence == False:
                tnr[ind, t] = tnr_[t][f]
                promi[ind, t] = prom[t][f]
            if prominence == True:
                if prom[t][f] == True:
                    tnr[ind, t] = tnr_[t][f]
                    promi[ind, t] = prom[t][f]

    t_tnr = ravel(t_tnr)

    return t_tnr, tnr, promi, freqs, time
