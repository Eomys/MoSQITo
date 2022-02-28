# -*- coding: utf-8 -*-

# Standard library imports
import numpy as np

from mosqito.sq_metrics.loudness.loudness_zwst._get_rns_index import _get_rns_index


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

    # From Ernesto Avedillo 13/feb/2022
    # Considering the original routine if ig > 7:ig = 7 until ig = 21 so I can append the last column until usl.shape = (18,21)
    usl_reshaped = np.append(usl, np.tile(
        usl[:, 7], 13).reshape(13, 18).T, axis=1)

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
    # Working array variables
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
        N_specific[zup_ea[i - 1]: zup_ea[i], :] = nm[i]

    N = np.zeros(data_length)

    # nm_aux = np.copy(nm)
    # nm_aux [0] = nm[1]

    # obtain the rns indexes for each value of the nm matrix.
    # rns_ind = _get_rns_index (nm, rns ,equal_too = True )
    rns_ind = _get_rns_index(nm, rns)
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
        n2_array_specific[zup_ea[i - 1]: zup_ea[i], :] = nm[i]
        dz_array_specific[zup_ea[i - 1]: zup_ea[i], :] = dz[i]
        z2_array_specific[zup_ea[i - 1]: zup_ea[i], :] = zup_array_ea[i]
        usl_array_specific[zup_ea[i - 1]: zup_ea[i], :] = usl_array[i]
        rns_values_specific[zup_ea[i - 1]: zup_ea[i], :] = rns_values[i]

    j = 1
    n1_aux = np.zeros(data_length)
    z1_aux = np.zeros(data_length)

    for i in np.arange(nm_wide):
        # for all cases where nm[i-1]>nm[i]
        j = zup_ea[i - 1]
        indexes = _get_rns_index(n2_array_specific[j - 1], rns)
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
                np.divide(n1_aux - Max_rns_nm_Array,
                          usl_array_specific[j]) + z1_aux,
                zup[i],
            )[mask_n1_bigger_nm]
            dz_array_specific[j, mask_n1_bigger_nm] = (z2_array_specific[j] - z1_aux)[
                mask_n1_bigger_nm
            ]
            n2_array_specific[j, mask_n1_bigger_nm] = (
                n1_aux -
                np.multiply(dz_array_specific[j], usl_array_specific[j])
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
                    indexes = _get_rns_index(
                        n2_array_specific[j,
                                          mask_z_bigger_z2], rns, equal_too=True
                    )
                    rns_values_specific[j, mask_z_bigger_z2] = rns[indexes]
                    usl_array_specific[j, mask_z_bigger_z2] = usl_reshaped[
                        indexes, i - 1
                    ]
                    # Save Copy de Z2 y N2
                    n1_aux[mask_z_bigger_z2] = n2_array_specific[j,
                                                                 mask_z_bigger_z2]
                    z1_aux[mask_z_bigger_z2] = z2_array_specific[j,
                                                                 mask_z_bigger_z2]

                    # Vuelvo al inicio del loop y reviso de nuevo que n2 sea menor que nm
                    # Vuelvo a calcular mask_n1_bigger_nm
                    # Para los valores de n1_aux<=nm[i]
                    mask_z_bigger_z2_1 = np.logical_and(
                        mask_z_bigger_z2,
                        np.round(n1_aux, dec_compare) <= np.round(
                            nm[i], dec_compare),
                    )
                    n2_array_specific[j, mask_z_bigger_z2_1] = nm[i,
                                                                  mask_z_bigger_z2_1]
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
                        np.round(n1_aux, dec_compare) > np.round(
                            nm[i], dec_compare),
                    )
                    Max_rns_nm_Array = np.maximum(
                        rns_values_specific[j], nm[i])
                    z2_array_specific[j, mask_z_bigger_z2_2] = np.minimum(
                        np.divide(n1_aux - Max_rns_nm_Array,
                                  usl_array_specific[j])
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
                        dz_array_specific[j] *
                        (n1_aux + n2_array_specific[j]) / 2
                    )[mask_z_bigger_z2_2]
                    N_specific[j, mask_z_bigger_z2_2] = (
                        n1_aux - np.multiply((z_array - z1_aux),
                                             usl_array_specific[j])
                    )[mask_z_bigger_z2_2]

                    # For the rest of the values  Where z < z2 calculate N_Specific
                    mask_z_rest = np.logical_xor(
                        mask_z_bigger_z2, mask_n1_bigger_nm)
                    N_specific[j, mask_z_rest] = (
                        n1_aux - np.multiply((z_array - z1_aux),
                                             usl_array_specific[j])
                    )[mask_z_rest]
                    z_array += 0.1

                    # Generate a new mask for n1 > nm[i]
                    mask_n1_bigger_nm = np.logical_xor(
                        mask_n1_bigger_nm, mask_z_bigger_z2_1
                    )

                else:
                    N_specific[j, mask_n1_bigger_nm] = (
                        n1_aux - np.multiply((z_array - z1_aux),
                                             usl_array_specific[j])
                    )[mask_n1_bigger_nm]
                    z_array += 0.1

                z1_aux = np.copy(z2_array_specific[j])
                n1_aux = np.copy(n2_array_specific[j])

                if mask_n1_bigger_nm.sum() == 0:
                    break
            z1_aux = np.copy(z2_array_specific[zup_ea[i] - 1])
            n1_aux = np.copy(n2_array_specific[zup_ea[i] - 1])

            indexes = _get_rns_index(
                n2_array_specific[j, mask_z_bigger_z2], rns, equal_too=True
            )
            rns_values_specific[j, mask_z_bigger_z2] = rns[indexes]
            usl_array_specific[j,
                               mask_z_bigger_z2] = usl_reshaped[indexes, i - 1]

    N[N < 0] = 0
    N[N <= 16] = np.floor(N[N <= 16] * 1000 + 0.5) / 1000
    N[N > 16] = np.floor(N[N > 16] * 100 + 0.5) / 100
    if len_1_nm:
        N = N[0]
        N_specific = N_specific[:, 0]

    return N, N_specific
