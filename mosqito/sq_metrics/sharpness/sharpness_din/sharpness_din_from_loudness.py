# -*- coding: utf-8 -*-
from numpy import interp, newaxis, array, where, linspace, ndarray, exp, ones, log, squeeze, sum

from mosqito.sq_metrics.sharpness.sharpness_din._weighting_fastl import x, y


def sharpness_din_from_loudness(N, N_specific, weighting="din"):
    """Acoustic sharpness calculation according to different methods
        (Aures, Von Bismarck, DIN 45692, Fastl) from time varying loudness.

    Parameters:
    ----------
    N : float or array_like
        Overall loudness [sones], size (Ntime,).
    N_specific : numpy.ndarray
        Specific loudness array [sones/bark], size (Nbark, Ntime).
    weighting : {'din', 'aures', 'bismarck', 'fastl'}
        Weighting function used for the sharpness computation. 
        Default is 'din'
    skip : float
        Duration to be cut at the beginning of the analysis in seconds.
        Default is 0
    Returns
    -------
    S : float or numpy.ndarray
        Sharpness value in [acum], dim (nseg)
    time_axis : numpy.array
        Time axis cut according to skip argument, size (Ntime,).

    See Also
    --------
    sharpness_din_tv : sharpness computation for a non-stationary time signal
    sharpness_din_st : sharpness computation for a stationary time signal
    sharpness_din_freq : sharpness computation from a sound spectrum
    sharpness_din_perseg : sharpness computation by time-segment

    Notes
    -----
    The different methods account for the weighting function applied on the specific loudness values:
     * DIN 45692 : weighting defined in the standard
     * Aures
     * Bismarck
     * Fastl

    References
    ----------
    .. [DIN45692] Measurement technique for the simulation of the auditory sensation of sharpness, 2009

    Examples
    --------
    .. plot::
       :include-source:

        >>> from mosqito.sq_metrics import loudness_zwtv, sharpness_din_from_loudness
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> f=1000
        >>> fs=48000
        >>> d=0.2
        >>> dB=60
        >>> time = np.arange(0, d, 1/fs)
        >>> f = np.linspace(1000,5000, len(time))
        >>> stimulus = 0.5 * (1 + np.sin(2 * np.pi * f * time))
        >>> rms = np.sqrt(np.mean(np.power(stimulus, 2)))
        >>> ampl = 0.00002 * np.power(10, dB / 20) / rms
        >>> stimulus = stimulus * ampl
        >>> N, N_spec, bark_axis, time_axis = loudness_zwtv(stimulus, fs=fs)
        >>> S = sharpness_din_from_loudness(N, N_spec)
        >>> plt.plot(time_axis, S)
        >>> plt.xlabel("Time [s]")
        >>> plt.ylabel("Sharpness [Acum]")
       
    Warning
    -------
    Note the transient effect at the beginning of the signal.
    """

    # 1D-array => 2D-array
    if not isinstance(N, ndarray):
        N = array([N])
    if N.ndim <= 1:
        ind = where(N < 0.1)
        N = N[newaxis, :]
    if N_specific.ndim <= 1:
        N_specific = N_specific[:, newaxis]

    # Bark axis
    z = linspace(0.1, 24, int(24 / 0.1))[:, newaxis]

    # weighting function
    if weighting == "din":
        g = ones(z.shape)
        g[z > 15.8] = 0.15 * exp(0.42 * (z[z > 15.8] - 15.8)) + 0.85
    elif weighting == "aures":
        g = 0.078 * (exp(0.171 * z) / z) * (N / log(N * 0.05 + 1))
    elif weighting == "bismarck":
        g = ones(z.shape)
        g[z > 15] = 0.2 * exp(0.308 * (z[z > 15] - 15)) + 0.8
    elif weighting == "fastl":
        g = interp(z, x, y)
    else:
        raise ValueError(
            "ERROR: weighting must be 'din', 'aures', 'bismarck' or 'fastl'")

    # S = zeros(N.shape)
    # ind = where(N >= 0.1)[1]
    S = 0.11 * sum(N_specific * g *
                      z * 0.1, axis=0) / N

    if S.size == 1:
        S = float(S)
    else:
        S = squeeze(S)
        S[ind] = 0
        
    return S

