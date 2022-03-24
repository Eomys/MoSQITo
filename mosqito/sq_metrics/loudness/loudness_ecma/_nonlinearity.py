import numpy as np


def _nonlinearity(p):
    """Apply the compressive nonlinearity of the auditory system to the
    rectified band pass signal rms values according to ECMA 418-2 section 5.1.7

    Parameters
    ----------
    p: numpy.array
        RMS value of the rectified band pass signal blocks

    Returns
    -------
    a_prime: numpy.array
        Specific Loudness [sone_HMS per Bark].

    """
    p_0 = 2e-5
    # c_N: In sones/bark
    c_N = 0.0217406
    alpha = 1.50
    v_i = np.array(
        [1.0, 0.6602, 0.0864, 0.6384, 0.0328, 0.4068, 0.2082, 0.3994, 0.6434]
    )
    thresh = np.array([15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0])
    p_ti = p_0 * 10 ** (thresh / 20)

    a_prime = np.ones(p.shape)
    for i in range(8):
        a_prime *= (1 + (p / p_ti[i]) ** alpha) ** ((v_i[i + 1] - v_i[i]) / alpha)
    a_prime *= c_N * p / p_0

    return a_prime