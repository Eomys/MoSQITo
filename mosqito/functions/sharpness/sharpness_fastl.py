# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 2020

@author: wantysal
"""

# Standard library imports
import numpy as np


def comp_sharpness_fastl(N, N_specific, is_stationary):
    """Sharpness calculation according to FASTL's method (1991)
        Expression for weighting function obtained by fitting an
        equation to the data given in 'Psychoacoustics: Facts and Models'

    Parameters
    ----------
    N : float
        loudness value
    N_specific : np.ndarray
        specific critical bands loudness
    is_stationary : boolean
        indicates if the signal is stationary or time-varying
    """
    # Bark axis
    z = np.linspace(0.1, 24, int(24 / 0.1))

    # Zwicker and Fastl weighting function
    x = np.array(
        [
            0.0985854,
            14.826764,
            15.364039,
            15.863559,
            16.297388,
            16.533346,
            16.844551,
            17.052244,
            17.335314,
            17.599474,
            17.816587,
            18.014925,
            18.231972,
            18.38313,
            18.543644,
            18.704224,
            18.883648,
            18.978205,
            19.167118,
            19.346476,
            19.441233,
            19.554567,
            19.668102,
            19.762926,
            19.923306,
            20.036907,
            20.188398,
            20.320976,
            20.462912,
            20.60518,
            20.78507,
            20.908228,
            21.078962,
            21.268276,
            21.410543,
            21.533966,
            21.704834,
            21.847036,
            21.98957,
            22.141394,
            22.312195,
            22.464752,
            22.62633,
            22.759441,
            22.89302,
            23.054932,
            23.236088,
            23.38871,
            23.5416,
            23.6848,
            23.932978,
        ]
    )

    y = np.array(
        [
            0.9783246,
            0.99701804,
            1.0092967,
            1.0169811,
            1.0438102,
            1.0713409,
            1.0891489,
            1.1167798,
            1.1441435,
            1.1668463,
            1.1944437,
            1.2268357,
            1.2497056,
            1.277537,
            1.3006072,
            1.3284053,
            1.3561363,
            1.3794405,
            1.411866,
            1.4348694,
            1.4723566,
            1.4908663,
            1.523559,
            1.5657737,
            1.5793887,
            1.6168091,
            1.6682787,
            1.7150875,
            1.7571354,
            1.8228214,
            1.8836461,
            1.9304883,
            2.0102572,
            2.0710485,
            2.1367345,
            2.2024875,
            2.2917116,
            2.35267,
            2.4372666,
            2.5123746,
            2.5968711,
            2.7239833,
            2.8226962,
            2.9073262,
            3.02505,
            3.147401,
            3.2980514,
            3.429891,
            3.5806417,
            3.7125149,
            3.9385738,
        ]
    )

    gZF = np.interp(z, x, y)

    if is_stationary == True:
        if N == 0:
            S = 0
        else:
            S = 0.11 * sum(N_specific * gZF * z * 0.1) / N
            print("Fastl sharpness:", "%.2f" % S, "acum")
    else:
        S = np.zeros((N.size))
        for t in range(N.size):
            if N[t] >= 0.1:
                S[t] = 0.11 * sum(N_specific[:, t] * gZF * z * 0.1) / N[t]

    return S
