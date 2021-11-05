import numpy as np


def loudness_function(p):

    """ NON-LINEARITY. SOUND PRESSURE INTO SPECIFIC LOUDNESS """
    p_0 = 2e-5
    # c_N: In sones/bark
    c_N = 0.0217406
    alpha = 1.50
    v_i = np.array(
        [1.0, 0.6602, 0.0864, 0.6384, 0.0328, 0.4068, 0.2082, 0.3994, 0.6434]
    )
    thresh = np.array([15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0])
    p_ti = p_0 * 10 ** (thresh / 20)
    # exp = (v_i[1:] - v_i[:-1]) / alpha
    # prod = np.prod(
    #     (1 + (p / p_ti[:, np.newaxis]) ** alpha)
    #     ** exp[:, np.newaxis],
    #     axis=0,
    # )
    # a_prime = c_N * p / p_0 * prod

    a_prime = np.ones(p.shape)
    for i in range(8):
        a_prime *= (1 + (p / p_ti[i]) ** alpha) ** ((v_i[i + 1] - v_i[i]) / alpha)
    a_prime *= c_N * p / p_0

    return a_prime


def loudness_function_alt(p):

    p_ref = np.array(
        [
            6.598919,
            8.838655,
            11.250792,
            14.17477,
            17.785425,
            20.533108,
            23.620234,
            26.878784,
            31.16102,
            35.784645,
            40.063473,
            44.85609,
            48.621613,
            53.92802,
            58.548725,
            64.02948,
            70.02354,
            76.3624,
            82.87268,
            87.32732,
            92.63762,
            97.607506,
            101.3779,
            104.46454,
        ]
    )

    loud_ref = np.array(
        [
            0.002630106,
            0.0051425043,
            0.010632731,
            0.021176357,
            0.047157302,
            0.076508306,
            0.11306698,
            0.17023043,
            0.2377996,
            0.32601807,
            0.3997006,
            0.50857294,
            0.6120943,
            0.8082804,
            0.9908526,
            1.4907696,
            2.2847574,
            3.9156787,
            6.8367267,
            10.09929,
            15.481487,
            25.099924,
            36.40073,
            52.800743,
        ]
    )

    a_prime = np.interp(p, 2e-5 * 10 ** (p_ref / 20), loud_ref)
    return a_prime