# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 12:22:23 2020

@author: wantysal
"""

# Standard library import
import numpy as np


def comp_sharpness_aures(N, N_specific, is_stationary):
    """Sharpness calculation

    The code is based on W. Aures' equation to determine sharpness
    from specific zwicker loudness.

    Parameters
    ----------
    N : float
        loudness value
    N_specific : np.ndarray
        specific critical bands loudness
    is_stationary : boolean
        indicates if the signal is stationary or time-varying

    Outputs
    -------
    S : sharpness
    """

    # Bark axis
    z = np.linspace(0.1, 24, int(24 / 0.1))

    if is_stationary == True:
        if N == 0:
            S = 0
        else:
            # weighting function depending on the loudness
            gA = np.zeros((z.size))
            gA = 0.078 * (np.exp(0.171 * z) / z) * (N / np.log(N * 0.05 + 1))
            S = 0.11 * sum(N_specific * gA * z * 0.1) / N
            print("Aures sharpness:", "%.2f" % S, "acum")
    else:
        S = np.zeros((N.size))
        gA = np.zeros((z.size, N.size))
        for t in range(N.size):
            if N[t] >= 0.1:
                # weighting function depending on the loudness
                gA[:, t] = (
                    0.078 * (np.exp(0.171 * z) / z) * (N[t] / np.log(N[t] * 0.05 + 1))
                )
                S[t] = 0.11 * sum(N_specific[:, t] * gA[:, t] * z * 0.1) / N[t]

    return S
