# -*- coding: utf-8 -*-

# External import
from numpy import argmin, abs

# Local imports
from mosqito.sq_metrics import loudness_zwtv
from mosqito.sq_metrics.sharpness.sharpness_din.sharpness_din_from_loudness import sharpness_din_from_loudness


def sharpness_din_tv(signal, fs, weighting="din", field_type="free", skip=0):
    """ 
    Returns the sharpness value 

    This function computes the sharpness value along time according to different methods.

    Parameters
    ----------
    signal: array_like
        Input time signal in [Pa], dim (nperseg, nseg)
    fs: float
        Sampling frequency
    weighting : {'din', 'aures', 'bismarck', 'fastl'}
        Weighting function used for the sharpness computation. 
        Default is 'din'
    field_type : {'free', 'diffuse'}
        Type of soundfield.
        Default is 'free'
    skip : float
        Number of second to be cut at the beginning of the analysis to skip the transient effect.
        Default is 0
        
    Returns
    -------
    S : numpy.array
        Sharpness value in [acum], dim (nseg)
    time_axis : numpy.array
        Time axis in [s]

    See Also
    --------
    .sharpness_din_from_loudness : Sharpness computation from loudness values
    .sharpness_din_st : Sharpness computation for a stationary time signal
    .sharpness_din_perseg : Sharpness computation by time-segment
    .sharpness_din_freq : Sharpness computation from a sound spectrum


    Notes
    -----
    When computing sharpness for a time-varying signal, a transient effect appears on the first points. To cut it, use *skip* argument.
    The different methods account for the weighting function applied on the specific loudness values:
     * DIN 45692 : weighting defined in the standard
     * Aures
     * Bismarck
     * Fastl

    References
    ----------
    :cite:empty:`S-DIN.45692:2009`
    :cite:empty:`S-ZF:9`
    :cite:empty:`S-B74`
    
    .. bibliography::
        :keyprefix: S-

    Examples
    --------
    .. plot::
       :include-source:

       >>> from mosqito.sq_metrics import sharpness_din_tv 
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
       >>> S, time_axis = sharpness_din_tv(stimulus, fs=fs, skip=0.1)
       >>> plt.plot(time_axis, S)
       >>> plt.xlabel("Time [s]")
       >>> plt.ylabel("Sharpness [Acum]")
    """
    if fs < 48000:
        print("[Warning] Signal resampled to 48 kHz to allow calculation. To fulfill the standard requirements fs should be >=48 kHz."
             )
        from scipy.signal import resample
        signal = resample(signal, int(48000 * len(signal) / fs))
        fs = 48000
    
    if skip == 0:
        print("[Warning] when computing sharpness from time-varying loudness, a transient effect appears on the first points. To cut it, use 'skip='")

    # Compute loudness
    N, N_specific, _, time_axis = loudness_zwtv(signal, fs, field_type)

    # Compute sharpness from loudness
    S = sharpness_din_from_loudness(
        N, N_specific, weighting=weighting)

    # Cut transient effect
    cut_index = argmin(abs(time_axis - skip))

    return S[cut_index:], time_axis[cut_index:]
