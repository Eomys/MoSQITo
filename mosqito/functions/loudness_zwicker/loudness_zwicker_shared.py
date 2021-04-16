# -*- coding: utf-8 -*-
"""
@date Created on Thur Apr 30 2020
@author martin_g for Eomys
"""

# Standard library imports
import numpy as np


def calc_main_loudness(spec_third, field_type):
    """Calculate core loudness

    The code is based on BASIC program published in "Program for
    calculating loudness according to DIN 45631 (ISO 532B)", E.Zwicker
    and H.Fastl, J.A.S.J (E) 12, 1 (1991).
    It also corresponds to the following functions of the C program
    published with ISO 532-1:2017:
    - corr_third_octave_intensities
    - f_calc_lcbs
    - f_calc_core_loudness
    - f_corr_loudness

    Parameters
    ----------
    spec_third : numpy.ndarray
        A third octave band spectrum [dB ref. 2e-5 Pa]
    field_type : str
        Type of soundfield correspondin to spec_third ("free" or
        "diffuse")

    Outputs
    -------
    nm :  numpy.ndarray
        Core loudness
    """
    #
    # Date tables definition (variable names and description according to
    # Zwicker:1991)
    # Ranges of 1/3 octave band levels for correction at low frequencies
    # according to equal loudness contours
    rap = np.array([45, 55, 65, 71, 80, 90, 100, 120])
    # Reduction of 1/3 octave band levels at low frequencies according to
    # equal loudness contours within the eight ranges defined by RAP
    dll = np.array(
        [
            (-32, -24, -16, -10, -5, 0, -7, -3, 0, -2, 0),
            (-29, -22, -15, -10, -4, 0, -7, -2, 0, -2, 0),
            (-27, -19, -14, -9, -4, 0, -6, -2, 0, -2, 0),
            (-25, -17, -12, -9, -3, 0, -5, -2, 0, -2, 0),
            (-23, -16, -11, -7, -3, 0, -4, -1, 0, -1, 0),
            (-20, -14, -10, -6, -3, 0, -4, -1, 0, -1, 0),
            (-18, -12, -9, -6, -2, 0, -3, -1, 0, -1, 0),
            (-15, -10, -8, -4, -2, 0, -3, -1, 0, -1, 0),
        ]
    )
    # Critical band level at absolute threshold without taking into
    # account the transmission characteristics of the ear
    ltq = np.array([30, 18, 12, 8, 7, 6, 5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    # Correction of levels according to the transmission characteristics
    # of the ear
    a0 = np.array(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.5, -1.6, -3.2, -5.4, -5.6, -4, -1.5, 2, 5, 12]
    )
    # Level difference between free and diffuse sound fields
    ddf = np.array(
        [
            0,
            0,
            0.5,
            0.9,
            1.2,
            1.6,
            2.3,
            2.8,
            3,
            2,
            0,
            -1.4,
            -2,
            -1.9,
            -1,
            0.5,
            3,
            4,
            4.3,
            4,
        ]
    )
    # Adaptation of 1/3 oct. band levels to the corresponding critical
    # band level
    dcb = np.array(
        [
            -0.25,
            -0.6,
            -0.8,
            -0.8,
            -0.5,
            0,
            0.5,
            1.1,
            1.5,
            1.7,
            1.8,
            1.8,
            1.7,
            1.6,
            1.4,
            1.2,
            0.8,
            0.5,
            0,
            -0.5,
        ]
    )
    #
    # Correction of 1/3 oct. band levels according to equal loudness
    # contours 'xp' and calculation of the intensities for 1/3 oct.
    # bands up to 315 Hz
    ti = np.zeros((dll.shape[1], 1))
    for i in np.arange(dll.shape[1]):
        j = 0
        while spec_third[i] > rap[j] - dll[j, i] and j < dll.shape[0]:
            j += 1
        xp = spec_third[i] + dll[j, i]
        ti[i] = np.power(10, (xp / 10))

    # Determination of levels LCB(1), LCB(2) and LCB(3) within the
    # first three critical bands
    gi = np.zeros(3)
    gi[0] = ti[0:6].sum()
    gi[1] = ti[6:9].sum()
    gi[2] = ti[9:11].sum()
    lcb = np.zeros(3)
    lcb[gi > 0] = 10 * np.log10(gi[gi > 0])

    # Calculation of main loudness
    s = 0.25
    nm = np.zeros(20)
    le = spec_third[8:]
    le = le.reshape((20))
    le[0:3] = lcb
    le = le - a0
    if field_type == "diffuse":
        le += ddf
    i = le > ltq
    le[i] -= dcb[i]
    mp1 = 0.0635 * np.power(10, 0.025 * ltq[i])
    mp2 = np.power(1 - s + s * np.power(10, 0.1 * (le[i] - ltq[i])), 0.25) - 1
    nm[i] = mp1 * mp2
    nm[nm < 0] = 0
    nm = np.append(nm, 0)
    #
    # Correction of specific loudness in the lowest critical band
    # taking into account the dependance of absolute threshold
    # within this critical band
    korry = 0.4 + 0.32 * nm[0] ** 0.2
    if korry <= 1:
        nm[0] *= korry
    return nm


def calc_slopes(nm):
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
