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

    # Prepare al arrays to work with
    if spec_third.ndim == 1:
        # This is for the test only for test_loudness_zwicker_3oct because only one array of one col is given and this routine needs 2 or more
        spec_third_adapted = (np.ones((spec_third.shape[0], 100)).T * spec_third).T
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


#
def get_rns_index(array_nm, vector_rns, equal_too=False):
    """Function that returns the index in the array vector_rns for each value of srray _nm

    Parameters
    ----------
    array_nm : numpy.ndarray, values of the matrix toget the indexes

    vector_rns:reference vector to get indexes
    equal_too : boolean

    Outputs
    -------
    indexes :  numpy.ndarray
        Array of indexes
    """

    if len(array_nm.shape) == 1:
        (wide,) = array_nm.shape
        (deep,) = vector_rns.shape
        array_aux = np.round(np.tile(array_nm, [deep, 1]), 8)
        rns_array = np.round(np.ones([wide, deep]) * vector_rns, 8).T
    else:
        wide, length = array_nm.shape
        (deep,) = vector_rns.shape
        array_aux = np.round(np.tile(array_nm, [deep, 1, 1]), 8)
        rns_array = np.round((np.ones([wide, length, deep]) * vector_rns), 8).transpose(
            2, 0, 1
        )
        # indexes = (array_aux < rns_array).sum(axis=0)
        # indexes[indexes==18] = 17
    if equal_too:
        indexes = (array_aux <= rns_array).sum(axis=0)
    else:
        indexes = (array_aux < rns_array).sum(axis=0)
    indexes[indexes == 18] = 17

    return indexes


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

    # From Ernesto Avedillo 13/feb/2022
    # Considering the original routine if ig > 7:ig = 7 until ig = 21 so I can append the last column until usl.shape = (18,21)
    usl_reshaped = np.append(usl, np.tile(usl[:, 7], 13).reshape(13, 18).T, axis=1)

    # For test, in case nm has only 1 col.
    len_1_nm = False
    if len(nm.shape) == 1:
        len_1_nm = True
        nm = np.append(nm, nm).reshape(2, 21).T

    # Start values
    data_length = nm.shape[1]
    nm_wide = nm.shape[0]
    spec_length = 240
    dec_compare = 8
    ## Working array variables
    n2_array_specific = np.ones((spec_length, data_length))
    z2_array_specific = np.ones((spec_length, data_length))
    usl_array_specific = np.ones((spec_length, data_length))
    dz_array_specific = np.ones((spec_length, data_length))
    rns_values_specific = np.ones((spec_length, data_length))
    # Create a zup vector called zup_ea to define the position in the N_spezific array.
    zup_ea = (np.copy(zup) * 10).astype(np.int32)
    zup_ea = np.append(zup_ea, 0)

    # Create a complete array of ZUP vectors with shape nm elements in a row
    zup_array_ea = (np.ones((nm_wide, data_length)).T * zup).T
    # crearte an array of z values 0.1 increase

    # Prepare the array N_specific for output
    # For all cases where nm[:,col-1] < nm[:,col]
    N_specific = np.zeros((spec_length, data_length))
    # I save the first values for first raws defined in zup_ea
    # N_specific[:zup_ea[0],:] = np.multiply(N_specific[:zup_ea[0],:] , nm[1])
    # I complete the rest of the matrix extending the array 21  to 240
    for i in np.arange(nm_wide - 1):
        N_specific[zup_ea[i - 1] : zup_ea[i], :] = nm[i]

    N = np.zeros(data_length)

    # nm_aux = np.copy(nm)
    # nm_aux [0] = nm[1]

    # obtain the rns indexes for each value of the nm matrix.
    # rns_ind = get_rns_index (nm, rns ,equal_too = True )
    rns_ind = get_rns_index(nm, rns)
    # save in an array the values corresponding to this index
    rns_values = rns[rns_ind]

    # search usl_array for each nm cell
    usl_array_ind = np.array(
        [rns_ind.T, np.ones((zup.shape[0], data_length)).T * np.arange(21)], dtype=int
    ).transpose(1, 2, 0)
    usl_array = usl_reshaped[usl_array_ind[:, :, 0], usl_array_ind[:, :, 1]].T
    # create a 240 x nm shape[1] array to save the dz values equal to z2-z1
    dz = np.zeros((nm_wide, data_length))
    dz = zup_array_ea - np.roll(zup_array_ea, 1, axis=0)

    dz[0, :] = zup[1]
    dz[1, :] = zup[1]

    for i in np.arange(nm_wide):
        n2_array_specific[zup_ea[i - 1] : zup_ea[i], :] = nm[i]
        dz_array_specific[zup_ea[i - 1] : zup_ea[i], :] = dz[i]
        z2_array_specific[zup_ea[i - 1] : zup_ea[i], :] = zup_array_ea[i]
        usl_array_specific[zup_ea[i - 1] : zup_ea[i], :] = usl_array[i]
        rns_values_specific[zup_ea[i - 1] : zup_ea[i], :] = rns_values[i]

    j = 1
    n1_aux = np.zeros(data_length)
    z1_aux = np.zeros(data_length)

    for i in np.arange(nm_wide):
        # for all cases where nm[i-1]>nm[i]
        j = zup_ea[i - 1]
        indexes = get_rns_index(n2_array_specific[j - 1], rns)
        rns_values_specific[j] = rns[indexes]
        usl_array_specific[j] = usl_reshaped[indexes, i - 1]

        mask_n1_bigger_nm = np.round(n2_array_specific[j - 1], dec_compare) > np.round(
            nm[i], dec_compare
        )
        # For all n1 <= nm[i] calculate (N = N + n2 * (z2 - z1))
        N[np.logical_not(mask_n1_bigger_nm)] += (
            n2_array_specific[j] * (z2_array_specific[j] - z1_aux)
        )[np.logical_not(mask_n1_bigger_nm)]
        n1_aux[np.logical_not(mask_n1_bigger_nm)] = np.copy(n2_array_specific[j])[
            np.logical_not(mask_n1_bigger_nm)
        ]
        z1_aux[np.logical_not(mask_n1_bigger_nm)] = np.copy(z2_array_specific[j])[
            np.logical_not(mask_n1_bigger_nm)
        ]

        if mask_n1_bigger_nm.sum() > 0:
            # For all n1 > nm[i] calculate z2,dz n2.
            # This routine
            # n2 = rns[j]
            # if n2 < nm[i]:
            #     n2 = nm[i]
            # dz = (n1 - n2) / usl[j, ig]
            # z2 = z1 + dz
            # if z2 > zup[i]:
            #     z2 = zup[i]
            #     dz = z2 - z1
            #     n2 = n1 - dz * usl[j, ig]
            # Can be subtituted by
            # max_rns_nm = max(rns[j],nm[i])
            # z2_ea = min((n1-max_rns_nm)/usl[j,ig]+z1,zup[i])
            # dz_ea = z2_ea - z1
            # n2_ea = n1 - dz_ea * usl[j,ig]

            Max_rns_nm_Array = np.maximum(rns_values_specific[j - 1], nm[i])
            z2_array_specific[j, mask_n1_bigger_nm] = np.minimum(
                np.divide(n1_aux - Max_rns_nm_Array, usl_array_specific[j]) + z1_aux,
                zup[i],
            )[mask_n1_bigger_nm]
            dz_array_specific[j, mask_n1_bigger_nm] = (z2_array_specific[j] - z1_aux)[
                mask_n1_bigger_nm
            ]
            n2_array_specific[j, mask_n1_bigger_nm] = (
                n1_aux - np.multiply(dz_array_specific[j], usl_array_specific[j])
            )[mask_n1_bigger_nm]

            # Calculate N for all n1 > nm[i]

            N[mask_n1_bigger_nm] += (
                dz_array_specific[j] * (n1_aux + n2_array_specific[j]) / 2
            )[mask_n1_bigger_nm]

            # get value of z
            z_array = np.ones(data_length) * zup[i - 1] + 0.1

            for j in np.arange(zup_ea[i - 1], zup_ea[i]):

                # Save values from previous calculation (only after second loop)
                if j != zup_ea[i - 1]:
                    z2_array_specific[j, mask_n1_bigger_nm] = z2_array_specific[
                        j - 1, mask_n1_bigger_nm
                    ]
                    n2_array_specific[j, mask_n1_bigger_nm] = n2_array_specific[
                        j - 1, mask_n1_bigger_nm
                    ]
                    dz_array_specific[j, mask_n1_bigger_nm] = dz_array_specific[
                        j - 1, mask_n1_bigger_nm
                    ]
                    usl_array_specific[j, mask_n1_bigger_nm] = usl_array_specific[
                        j - 1, mask_n1_bigger_nm
                    ]
                    rns_values_specific[j, mask_n1_bigger_nm] = rns_values_specific[
                        j - 1, mask_n1_bigger_nm
                    ]

                # Sometimes a second loop is necesary if z > z2
                mask_z_bigger_z2 = np.logical_and(
                    mask_n1_bigger_nm,
                    np.round(z2_array_specific[j], dec_compare)
                    <= np.round(z_array, dec_compare),
                )
                if mask_z_bigger_z2.sum() > 0:
                    indexes = get_rns_index(
                        n2_array_specific[j, mask_z_bigger_z2], rns, equal_too=True
                    )
                    rns_values_specific[j, mask_z_bigger_z2] = rns[indexes]
                    usl_array_specific[j, mask_z_bigger_z2] = usl_reshaped[
                        indexes, i - 1
                    ]
                    # Save Copy de Z2 y N2
                    n1_aux[mask_z_bigger_z2] = n2_array_specific[j, mask_z_bigger_z2]
                    z1_aux[mask_z_bigger_z2] = z2_array_specific[j, mask_z_bigger_z2]

                    # Vuelvo al inicio del loop y reviso de nuevo que n2 sea menor que nm
                    # Vuelvo a calcular mask_n1_bigger_nm
                    # Para los valores de n1_aux<=nm[i]
                    mask_z_bigger_z2_1 = np.logical_and(
                        mask_z_bigger_z2,
                        np.round(n1_aux, dec_compare) <= np.round(nm[i], dec_compare),
                    )
                    n2_array_specific[j, mask_z_bigger_z2_1] = nm[i, mask_z_bigger_z2_1]
                    z2_array_specific[j, mask_z_bigger_z2_1] = zup[i]
                    dz_array_specific[j, mask_z_bigger_z2_1] = (
                        z2_array_specific[j] - z1_aux
                    )[mask_z_bigger_z2_1]
                    # Recalculate N
                    N[mask_z_bigger_z2_1] += (
                        n2_array_specific[j] * (z2_array_specific[j] - z1_aux)
                    )[mask_z_bigger_z2_1]

                    # For Values n1_aux>nm[i] after second loop
                    mask_z_bigger_z2_2 = np.logical_and(
                        mask_z_bigger_z2,
                        np.round(n1_aux, dec_compare) > np.round(nm[i], dec_compare),
                    )
                    Max_rns_nm_Array = np.maximum(rns_values_specific[j], nm[i])
                    z2_array_specific[j, mask_z_bigger_z2_2] = np.minimum(
                        np.divide(n1_aux - Max_rns_nm_Array, usl_array_specific[j])
                        + z1_aux,
                        zup[i],
                    )[mask_z_bigger_z2_2]
                    dz_array_specific[j, mask_z_bigger_z2_2] = (
                        z2_array_specific[j] - z1_aux
                    )[mask_z_bigger_z2_2]
                    n2_array_specific[j, mask_z_bigger_z2_2] = (
                        n1_aux
                        - np.multiply(dz_array_specific[j], usl_array_specific[j])
                    )[mask_z_bigger_z2_2]
                    # Recalculate N
                    N[mask_z_bigger_z2_2] += (
                        dz_array_specific[j] * (n1_aux + n2_array_specific[j]) / 2
                    )[mask_z_bigger_z2_2]
                    N_specific[j, mask_z_bigger_z2_2] = (
                        n1_aux - np.multiply((z_array - z1_aux), usl_array_specific[j])
                    )[mask_z_bigger_z2_2]

                    # For the rest of the values  Where z < z2 calculate N_Specific
                    mask_z_rest = np.logical_xor(mask_z_bigger_z2, mask_n1_bigger_nm)
                    N_specific[j, mask_z_rest] = (
                        n1_aux - np.multiply((z_array - z1_aux), usl_array_specific[j])
                    )[mask_z_rest]
                    z_array += 0.1

                    # Generate a new mask for n1 > nm[i]
                    mask_n1_bigger_nm = np.logical_xor(
                        mask_n1_bigger_nm, mask_z_bigger_z2_1
                    )

                else:
                    N_specific[j, mask_n1_bigger_nm] = (
                        n1_aux - np.multiply((z_array - z1_aux), usl_array_specific[j])
                    )[mask_n1_bigger_nm]
                    z_array += 0.1

                z1_aux = np.copy(z2_array_specific[j])
                n1_aux = np.copy(n2_array_specific[j])

                if mask_n1_bigger_nm.sum() == 0:
                    break
            z1_aux = np.copy(z2_array_specific[zup_ea[i] - 1])
            n1_aux = np.copy(n2_array_specific[zup_ea[i] - 1])

            indexes = get_rns_index(
                n2_array_specific[j, mask_z_bigger_z2], rns, equal_too=True
            )
            rns_values_specific[j, mask_z_bigger_z2] = rns[indexes]
            usl_array_specific[j, mask_z_bigger_z2] = usl_reshaped[indexes, i - 1]

    N[N < 0] = 0
    N[N <= 16] = np.floor(N[N <= 16] * 1000 + 0.5) / 1000
    N[N > 16] = np.floor(N[N > 16] * 100 + 0.5) / 100
    if len_1_nm:
        N = N[0]
        N_specific = N_specific[:, 0]

    return N, N_specific
