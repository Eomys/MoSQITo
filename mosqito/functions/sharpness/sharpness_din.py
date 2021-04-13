# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:59:53 2020

@author: wantysal
"""
# Standard library import
import numpy as np


def comp_sharpness_din(N, N_specific, is_stationary):
    """Sharpness calculation

    The code is based on DIN 45692:2009 to determine sharpness
    from specific zwicker loudness.

    Parameters
    ----------
    N : float
        loudness value
    N_specific : np.ndarray
        specific critical bands loudness
    is_stationary : boolean
        indicates if the signal is stationary or time-varying
    time : np.array
        time axis

    Outputs
    -------
    S : sharpness
    """

    # Bark axis
    z = np.linspace(0.1, 24, int(24 / 0.1))

    # weighting function
    gDIN = np.zeros((z.size))
    gDIN[z <= 15.8] = 1
    gDIN[z > 15.8] = 0.15 * np.exp(0.42 * (z[z > 15.8] - 15.8)) + 0.85

    if is_stationary:
        if N == 0:
            S = 0
        else:
            S = 0.11 * sum(N_specific * gDIN * z * 0.1) / N
            print("DIN sharpness:", "%.2f" % S, "acum")
    else:
        S = np.zeros((N.size))
        for t in range(N.size):
            if N[t] >= 0.1:
                S[t] = 0.11 * sum(N_specific[:, t] * gDIN * z * 0.1) / N[t]
    return S
