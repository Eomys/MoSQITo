# -*- coding: utf-8 -*-

import numpy as np

from mosqito.sq_metrics.sharpness.sharpness_din._weighting_fastl import x, y


def sharpness_din_st_from_loudness(N, N_specific, weighting="din"):
    """Acoustic sharpness calculation according to different methods
        (Aures, Von Bismarck, DIN 45692, Fastl) from stationary loudness.

    Parameters:
    ----------
    N : float or numpy.ndarray
        The overall loudness [sones]. If array, size (Nseg,)
    N_specific : numpy.ndarray
        The specific loudness array [sones/bark], size (Nbark,) or (Nbark, Nseg)
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'

    Outputs
    ------
    S : float or numpy.ndarray
        Sharpness value. If input is an array, output size is (Nseg,)

    """

    # 1D-array => 2D-array
    if not isinstance(N, np.ndarray):
        N = np.array([N])
    if N.ndim <= 1:
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
        raise ValueError("ERROR: weighting must be 'din', 'aures', 'bismarck' or 'fastl'")

    S = np.zeros(N.shape)
    ind = np.where(N >= 0.1)[0]
    S[ind] =  0.11* np.sum( N_specific[:,ind] * g * z * 0.1, axis=0)/ N[:,ind]
    

    if S.size == 1:
        S = float(S)
    else:
        S = np.squeeze(S)
        
    return S