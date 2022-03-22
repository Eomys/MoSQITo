# -*- coding: utf-8 -*-

import numpy as np


def sharpness_din_from_loudness(N, N_specific, weighting="din", skip=0):
    """Acoustic sharpness calculation according to different methods:
        Aures, Von Bismarck, DIN 45692, Fastl

    Parameters:
    ----------
    N : float or numpy.ndarray
        The overall loudness [sones]. If array, size (Ntime,)
    N_specific : numpy.ndarray
        The specific loudness array [sones/bark], size (Nbark,) or (Nbark, Ntime)
    weighting : string
        To specify the weighting function used for the
        sharpness computation.'din' by default,'aures', 'bismarck','fastl'
    skip : float
        number of second to be cut at the beginning of the analysis

    Outputs
    ------
    S : float or numpy.ndarray
        sharpness value

    """

    # Bark axis
    z = np.linspace(0.1, 24, int(24 / 0.1))

    # weighting function
    gDIN = np.ones(z.shape)
    gDIN[z > 15.8] = 0.15 * np.exp(0.42 * (z[z > 15.8] - 15.8)) + 0.85

    # Formating of stationnary signal data
    if not isinstance(N, np.ndarray):
        N = np.array([N])
    if N_specific.ndim <= 1:
        N_specific = N_specific[:, np.newaxis]
    else:
        gDIN = gDIN[:, np.newaxis]
        z = z[:, np.newaxis]

    S = np.zeros(N.shape)
    ind = np.where(N >= 0.1)[0]
    S[ind] = (
        0.11
        * np.sum(
            np.squeeze(N_specific[:, ind]) * gDIN * z * 0.1,
            axis=0,
        )
        / N[ind]
    )

    if S.size == 1:
        S = float(S)
    return S