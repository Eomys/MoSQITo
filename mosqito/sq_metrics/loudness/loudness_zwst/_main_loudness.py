# -*- coding: utf-8 -*-
"""
@date Created on Thur Apr 30 2020
@author martin_g for Eomys
"""

# Standard library imports
import numpy as np


def _main_loudness(spec_third, field_type):
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
    # Ref. ISO 532-1:2017 paragraph A.3
    # The table A.3 giving the weights of the 1/3 band levels for
    # center freq. below 300 Hz is only specified for levels up to 120 dB
    # If one of the first 11 bands (from 25 to 250 Hz) exceed 120 dB the
    # Zwicker method cannot be applied.
    if np.max(spec_third[0:11]) > 120.0:
        raise ValueError(
            "1/3 octave band value exceed 120 dB, for which "
            + "the Zwicker method is no longer valid."
        )
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
    ltq = np.array([30, 18, 12, 8, 7, 6, 5, 4, 3,
                    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    # Correction of levels according to the transmission characteristics
    # of the ear
    a0 = np.array(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.5, -
            1.6, -3.2, -5.4, -5.6, -4, -1.5, 2, 5, 12]
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

    # Prepare al arrays to work with
    if spec_third.ndim == 1:
        # This is for the test only for test_loudness_zwicker_3oct because only one array of one col is given and this routine needs 2 or more
        spec_third_adapted = (
            np.ones((spec_third.shape[0], 100)).T * spec_third).T
    elif spec_third.shape[1] == 1:
        # This line is only for testing test_loudness_zwicker_wav(), only in case one col in spec third is given.
        spec_third_adapted = (
            np.ones((spec_third.shape[0], 100)).T * spec_third[:, 0]
        ).T
    else:
        # Fomn common wav files where more htan one col is given.
        spec_third_adapted = spec_third

    spec_third_aux = spec_third_adapted[: dll.shape[1], :]
    spec_third_aux[:, -1] = 0

    # Convert rap, dll in 3 dimensional array
    # 1. generate the array shape
    base_mat = np.ones((dll.shape[0], dll.shape[1], spec_third_aux.shape[1]))
    # 2. start saving data in rap and DLL array
    rap_mat = np.array(
        [base_mat[:, i, :].T * rap for i in np.arange(dll.shape[1])]
    ).transpose(2, 0, 1)
    dll_mat = np.array(
        [
            np.multiply(base_mat[:, :, i], dll)
            for i in np.arange(spec_third_adapted.shape[1])
        ]
    ).transpose(1, 2, 0)
    spec_third_aux_mat = np.array(
        [
            np.multiply(base_mat[i, :, :], spec_third_aux)
            for i in np.arange(dll.shape[0])
        ]
    )
    # create the the array rap-dll
    rap_dll_mat = rap_mat - dll_mat

    # This part substitutes the while loop.
    # create the mask to operate
    logic_mat = spec_third_aux_mat > rap_dll_mat
    dll_result = dll_mat[0, :, :]
    dll_result[logic_mat[0, :, :]] = 0
    for i in np.arange(1, dll_mat.shape[0] - 1):
        mask = np.logical_xor(logic_mat[i - 1, :, :], logic_mat[i, :, :])
        dll_result[mask] = dll_mat[i, mask]

    xp = dll_result + spec_third_aux
    ti = np.power(10, (xp / 10))

    # Determination of levels LCB(1), LCB(2) and LCB(3) within the
    # first three critical bands

    gi = np.zeros([3, dll_result.shape[1]])
    gi[0, :] = ti[0:6, :].sum(axis=0)
    gi[1, :] = ti[6:9, :].sum(axis=0)
    gi[2, :] = ti[9:11, :].sum(axis=0)

    logic_gi = gi > 0
    lcb = np.zeros([3, dll_result.shape[1]])
    lcb = 10 * np.log10(gi[logic_gi])
    lcb = lcb.reshape(3, dll_result.shape[1])

    # Calculation of main loudness
    s = 0.25
    nm = np.zeros([20, spec_third_aux.shape[1]])
    le = np.copy(spec_third_adapted[8:, :])
    # le = le.reshape((20))
    le[0:3, :] = lcb
    a0_mat = np.ones(a0.shape[0] * spec_third_adapted.shape[1]).reshape(
        a0.shape[0], spec_third_adapted.shape[1]
    )
    a0_mat = (a0_mat.T * a0).T
    le = le - a0_mat

    if field_type == "diffuse":
        ddf_mat = np.ones(ddf.shape[0] * spec_third_adapted.shape[1]).reshape(
            ddf.shape[0], spec_third_adapted.shape[1]
        )
        ddf_mat = (ddf_mat.T * ddf).T
        le += ddf_mat

    ltq_mat = np.ones(ltq.shape[0] * spec_third_adapted.shape[1]).reshape(
        ltq.shape[0], spec_third_adapted.shape[1]
    )
    ltq_mat = (ltq_mat.T * ltq).T
    i = le > ltq_mat
    dcb_mat = np.ones(dcb.shape[0] * spec_third_adapted.shape[1]).reshape(
        dcb.shape[0], spec_third_adapted.shape[1]
    )
    dcb_mat = (dcb_mat.T * dcb).T
    le[i] -= dcb_mat[i]

    mp1 = 0.0635 * np.power(10, 0.025 * ltq_mat)
    mp1[i == False] = 0
    mp2 = np.power(1 - s + s * np.power(10, 0.1 * (le - ltq_mat)), 0.25) - 1
    mp2[i == False] = 0

    nm = np.multiply(mp1, mp2)

    nm[i == False] = 0
    nm[nm < 0] = 0
    current_shape = nm.shape
    nm = np.append(nm, np.zeros(current_shape[1])).reshape(
        current_shape[0] + 1, current_shape[1]
    )
    #
    # Correction of specific loudness in the lowest critical band
    # taking into account the dependance of absolute threshold
    # within this critical band
    korry = 0.4 + 0.32 * nm[0] ** 0.2
    nm[0, korry <= 1] *= korry
    nm[:, -1] = 0
    if spec_third.ndim == 1 or spec_third.shape[1] == 1:
        # This is only for test_loudness_zwicker_3oct because only one array of one col is given and this routine needs 2 or more
        # This line is only also for testing test_loudness_zwicker_wav(), only in case one col in spec third is given.
        nm = nm[:, 1]

    return nm
