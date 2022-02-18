# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np


def _calc_slopes(nm):
    """"""
    # Upper limits of approximated critical bands in terms of critical
    # band rate
    zup = np.array(
        [
            0.9,
            1.8,
            2.8,
            3.5,
            4.4,
            5.4,
            6.6,
            7.9,
            9.2,
            10.6,
            12.3,
            13.8,
            15.2,
            16.7,
            18.1,
            19.3,
            20.6,
            21.8,
            22.7,
            23.6,
            24,
        ]
    )
    # Range of specific loudness for the determination of the steepness
    # of the upper slopes in the specific loudness - critical band rate
    # pattern
    rns = np.array(
        [
            21.5,
            18,
            15.1,
            11.5,
            9,
            6.1,
            4.4,
            3.1,
            2.13,
            1.36,
            0.82,
            0.42,
            0.30,
            0.22,
            0.15,
            0.10,
            0.035,
            0,
        ]
    )
    # Steepness of the upper slopes in the specific loudness = Critical
    # band rate pattern for the ranges 'rns' as a function of the number
    # of the critical band
    usl = np.array(
        [
            (13, 8.2, 6.3, 5.5, 5.5, 5.5, 5.5, 5.5),
            (9, 7.5, 6, 5.1, 4.5, 4.5, 4.5, 4.5),
            (7.8, 6.7, 5.6, 4.9, 4.4, 3.9, 3.9, 3.9),
            (6.2, 5.4, 4.6, 4.0, 3.5, 3.2, 3.2, 3.2),
            (4.5, 3.8, 3.6, 3.2, 2.9, 2.7, 2.7, 2.7),
            (3.7, 3.0, 2.8, 2.35, 2.2, 2.2, 2.2, 2.2),
            (2.9, 2.3, 2.1, 1.9, 1.8, 1.7, 1.7, 1.7),
            (2.4, 1.7, 1.5, 1.35, 1.3, 1.3, 1.3, 1.3),
            (1.95, 1.45, 1.3, 1.15, 1.1, 1.1, 1.1, 1.1),
            (1.5, 1.2, 0.94, 0.86, 0.82, 0.82, 0.82, 0.82),
            (0.72, 0.67, 0.64, 0.63, 0.62, 0.62, 0.62, 0.62),
            (0.59, 0.53, 0.51, 0.50, 0.42, 0.42, 0.42, 0.42),
            (0.40, 0.33, 0.26, 0.24, 0.24, 0.22, 0.22, 0.22),
            (0.27, 0.21, 0.20, 0.18, 0.17, 0.17, 0.17, 0.17),
            (0.16, 0.15, 0.14, 0.12, 0.11, 0.11, 0.11, 0.11),
            (0.12, 0.11, 0.10, 0.08, 0.08, 0.08, 0.08, 0.08),
            (0.09, 0.08, 0.07, 0.06, 0.06, 0.06, 0.06, 0.05),
            (0.06, 0.05, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02),
        ]
    )

    #
    # Start values
    j = 0
    N = 0
    z1 = 0
    n1 = 0
    iz = 0
    z = 0.1
    N_specific = np.zeros(int(24 / 0.1))
    #
    # Step to first and subsequent critical bands
    for i in np.arange(21):
        zup[i] += 0.0001
        ig = i - 1
        if ig > 7:
            ig = 7
        while z1 < zup[i]:
            if n1 <= nm[i]:
                if n1 < nm[i]:
                    #
                    # Determination of the number j corresponding to the range
                    # of specific loudness
                    j = 0
                    while rns[j] > nm[i] and j < 17:
                        j += 1
                #
                # Contribution of unmasked main loudness to total loudness
                # and calculation of values N_specific(iz) with a spacing of
                # z = iz * 0.1 bark
                z2 = zup[i]
                n2 = nm[i]
                N = N + n2 * (z2 - z1)
                while z < z2:
                    N_specific[iz] = n2
                    iz += 1
                    z += 0.1
            else:
                #
                # Decision wether the critical band in question is completely
                # or partially masked by accessory loudness
                n2 = rns[j]
                if n2 < nm[i]:
                    n2 = nm[i]
                dz = (n1 - n2) / usl[j, ig]
                z2 = z1 + dz
                if z2 > zup[i]:
                    z2 = zup[i]
                    dz = z2 - z1
                    n2 = n1 - dz * usl[j, ig]
                #
                # Contribution of accessory loudness to total loudness
                N = N + dz * (n1 + n2) / 2
                while z < z2:
                    N_specific[iz] = n1 - (z - z1) * usl[j, ig]
                    iz += 1
                    z += 0.1
            #
            # Step to next segment
            while n2 <= rns[j] and j < 17:
                j += 1
            if n2 <= rns[j] and j >= 17:
                j = 17
            z1 = z2
            n1 = n2
    #
    # Final correction
    if N < 0:
        N = 0
    if N <= 16:
        N = np.floor(N * 1000 + 0.5) / 1000
    else:
        N = np.floor(N * 100 + 0.5) / 100

    return N, N_specific
