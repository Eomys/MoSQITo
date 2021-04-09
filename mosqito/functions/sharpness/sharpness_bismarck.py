# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:06:11 2020

@author: wantysal
"""

# Standard library import
import numpy as np


def comp_sharpness_bismarck(N, N_specific, is_stationary):
    """Sharpness calculation

    The code is based on Bismarck formulation to determine sharpness
    from specific zwicker loudness. It is quite similar to DIN 45692:2009.

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

    # Von Bismarck weighting function
    gB = np.zeros((z.size))
    gB[z <= 15] = 1
    gB[z > 15] = 0.2 * np.exp(0.308 * (z[z > 15] - 15)) + 0.8

    if is_stationary:
        if N == 0:
            S = 0
        else:
            S = 0.11 * sum(N_specific * gB * z * 0.1) / N
            print("Bismarck sharpness:", "%.2f" % S, "acum")
    else:
        S = np.zeros((N.size))
        for t in range(N.size):
            if N[t] >= 0.1:
                S[t] = 0.11 * sum(N_specific[:, t] * gB * z * 0.1) / N[t]
    return S
