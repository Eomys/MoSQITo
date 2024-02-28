# -*- coding: utf-8 -*-

import numpy as np

from mosqito.sq_metrics.sharpness.sharpness_din._weighting_fastl import x, y


def sharpness_din_from_loudness(N, N_specific, weighting="din", skip=0):
    """Acoustic sharpness calculation according to different methods
        (Aures, Von Bismarck, DIN 45692, Fastl) from time varying loudness.

    Parameters:
    ----------
    N : float or numpy.ndarray
        The overall loudness [sones], size (Ntime,).
    N_specific : numpy.ndarray
        The specific loudness array [sones/bark], size (Nbark, Ntime).
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    skip : float
        number of second to be cut at the beginning of the analysis

    Outputs
    ------
    S : float or numpy.ndarray
        Sharpness value, size (Ntime,).
    time_axis : numpy.array
        Time axis cut according to skip, size (Ntime,).

    """

    # 1D-array => 2D-array
    if not isinstance(N, np.ndarray):
        N = np.array([N])
    if N.ndim <= 1:
        ind = np.where(N < 0.1)
        N = N[np.newaxis, :]
    if N_specific.ndim <= 1:
        N_specific = N_specific[:, np.newaxis]

    # Bark axis
    z = np.linspace(0.1, 24, int(24 / 0.1))[:, np.newaxis]

    # weighting function
    if weighting == "din":
        g = np.ones(z.shape)
        g[z > 15.8] = 0.15 * np.exp(0.42 * (z[z > 15.8] - 15.8)) + 0.85
    elif weighting == "aures":
        g = 0.078 * (np.exp(0.171 * z) / z) * (N / np.log(N * 0.05 + 1))
    elif weighting == "bismarck":
        g = np.ones(z.shape)
        g[z > 15] = 0.2 * np.exp(0.308 * (z[z > 15] - 15)) + 0.8
    elif weighting == "fastl":
        g = np.interp(z, x, y)
    else:
        raise ValueError(
            "ERROR: weighting must be 'din', 'aures', 'bismarck' or 'fastl'")

    # S = np.zeros(N.shape)
    # ind = np.where(N >= 0.1)[1]
    S = 0.11 * np.sum(N_specific * g *
                      z * 0.1, axis=0) / N

    if S.size == 1:
        S = S.flat[0]
    else:
        S = np.squeeze(S)
        S[ind] = 0

    return S
